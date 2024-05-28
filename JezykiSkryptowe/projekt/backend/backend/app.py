import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import desc, select

from backend.agents.agent import parse_message_with_stream

from backend.api.deps import SessionDep
from backend.agents.rag import qdrant_client
from backend.agents.title_agent import generate_title
from backend.models import (
    Message,
    MessageKind,
    MessagePublic,
    SentBy,
    Thread,
    ThreadPublicWithMessages,
)
from backend.api.file_router import file_router
from qdrant_client.http import models as rest
from langchain_core.messages import AIMessageChunk
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)

if not qdrant_client.collection_exists("docs"):
    qdrant_client.create_collection(
        "docs",
        vectors_config=rest.VectorParams(
            size=1536,
            distance=rest.Distance.COSINE,
        ),
    )


@app.get("/messages", response_model=list[MessagePublic])
async def messages(session: SessionDep):
    messages = select(Message).limit(10)

    return session.exec(messages).all()


@app.get("/threads", response_model=list[ThreadPublicWithMessages])
async def threads(session: SessionDep):
    threads = select(Thread).order_by(desc(Thread.created_at)).limit(100)

    return session.exec(threads).all()


@app.websocket("/chat/{thread_id}")
async def chat_endpoint(websocket: WebSocket, session: SessionDep, thread_id: str):
    await websocket.accept()

    does_exist = session.exec(
        select(Thread).where(Thread.id == thread_id)
    ).one_or_none()

    while True:
        user_message = await websocket.receive_json()

        if not does_exist:
            title = generate_title(user_message["content"])
            thread = Thread(id=thread_id, title=title)
            session.add(thread)
            session.commit()

            does_exist = session.exec(
                select(Thread).where(Thread.id == thread_id)
            ).one_or_none()

        message_stream = parse_message_with_stream(user_message["content"], thread_id)

        session.add(
            Message(
                id=user_message["id"],
                content=user_message["content"],
                thread_id=thread_id,
                sent_by=SentBy.user,
            )
        )

        bot_messages_by_id = {}

        async for event in message_stream:
            kind = event["event"]

            if kind == "on_chat_model_stream":
                event_data: AIMessageChunk = event["data"].get("chunk", None)
                bot_messages_by_id[event["run_id"]] = (
                    bot_messages_by_id.get(event["run_id"], "") + event_data.content
                )

                message = Message(
                    id=event_data.id,
                    content=bot_messages_by_id[event["run_id"]],
                    thread_id=thread_id,
                    sent_by=SentBy.bot,
                )

                if (
                    event_data.response_metadata
                    and bot_messages_by_id[event["run_id"]] != ""
                ):
                    session.add(
                        message,
                    )

                await websocket.send_json(
                    message.model_dump(),
                )

            if kind == "on_tool_start":
                tool_input = event["data"].get("input", "")
                message = Message(
                    id=event["run_id"] + "_input",
                    content=json.dumps(tool_input),
                    thread_id=thread_id,
                    sent_by=SentBy.bot,
                    kind=MessageKind.tool_start,
                    tool_name=event["name"],
                )
                await websocket.send_json(message.model_dump())

                session.add(message)

            if kind == "on_tool_end":
                tool_output = event["data"].get("output", "")

                if isinstance(tool_output, dict):
                    parsed_output = json.dumps(tool_output)
                elif isinstance(tool_output, list):
                    if all(isinstance(i, Document) for i in tool_output):
                        new_value: list[Document] = tool_output
                        parsed_output = json.dumps([i.dict() for i in new_value])
                    else:
                        parsed_output = json.dumps(tool_output)
                else:
                    parsed_output = json.dumps(tool_output)

                message = Message(
                    id=event["run_id"] + "_output",
                    content=parsed_output,
                    thread_id=thread_id,
                    sent_by=SentBy.bot,
                    kind=MessageKind.tool_output,
                    tool_name=event["name"],
                )
                session.add(
                    message,
                )

                await websocket.send_json(message.model_dump())

        session.commit()
