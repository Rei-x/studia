import json
import os
from uuid import uuid4
from fastapi import FastAPI, UploadFile, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import desc, select

from backend.agents.agent import parse_message_with_stream
from dotenv import load_dotenv

from backend.api.deps import SessionDep
from backend.agents.rag import process_file_with_unstructured, qdrant_client
from backend.agents.title_agent import generate_title
from backend.models import (
    File,
    FilePublic,
    Message,
    MessagePublic,
    SentBy,
    Thread,
    ThreadPublicWithMessages,
)
from qdrant_client.http import models as rest
from langchain_core.messages import AIMessageChunk


load_dotenv()
app = FastAPI()


class ResponseModel(BaseModel):
    message: str


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not qdrant_client.collection_exists("docs"):
    qdrant_client.create_collection(
        "docs",
        vectors_config=rest.VectorParams(
            size=1536,
            distance=rest.Distance.COSINE,
        ),
    )


@app.get("/", response_model=ResponseModel)
async def root():
    return {"message": "Hello World"}


@app.get("/messages", response_model=list[MessagePublic])
async def messages(session: SessionDep):
    messages = select(Message).limit(10)

    return session.exec(messages).all()


@app.get("/files", response_model=list[FilePublic])
async def files(session: SessionDep):
    return session.exec(select(File).order_by(desc(File.created_at)).limit(100)).all()


@app.delete("/files/{file_id}", response_model=ResponseModel)
async def delete_file(file_id: str, session: SessionDep):
    file = session.exec(select(File).where(File.id == file_id)).one_or_none()

    if not file:
        return {"message": "File not found"}

    os.remove(file.on_disk)

    session.delete(file)
    qdrant_client.delete(
        "docs",
        points_selector=rest.FilterSelector(
            filter=rest.Filter(
                must=[
                    rest.FieldCondition(
                        key="metadata.id", match=rest.MatchValue(value=file_id)
                    )
                ]
            )
        ),
    )
    session.commit()

    return {"message": "File deleted successfully"}


@app.get("/threads", response_model=list[ThreadPublicWithMessages])
async def threads(session: SessionDep):
    threads = select(Thread).order_by(desc(Thread.created_at)).limit(100)

    return session.exec(threads).all()


upload_dir = "uploads"


@app.post("/upload")
async def upload_file(files: list[UploadFile], session: SessionDep):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    for file in files:
        contents = await file.read()
        file_size = len(contents)

        if not file.filename:
            return {"message": "No file uploaded"}

        random_filename = f"{uuid4()}"
        with open(f"{upload_dir}/{random_filename}_{file.filename}", "wb") as f:
            f.write(contents)
        new_file = File(
            id=uuid4().hex,
            filename=file.filename,
            on_disk=f"{upload_dir}/{random_filename}_{file.filename}",
            size=file_size,
        )
        session.add(new_file)

        if not new_file.id:
            return {"message": "File not saved"}

        await process_file_with_unstructured(contents, file.filename, id=new_file.id)
        session.commit()

    return {"message": "Files uploaded successfully"}


@app.websocket("/chat/{thread_id}")
async def chat_endpoint(websocket: WebSocket, session: SessionDep, thread_id: str):
    await websocket.accept()

    does_exist = session.exec(
        select(Thread).where(Thread.id == thread_id)
    ).one_or_none()

    while True:
        user_message = json.loads(await websocket.receive_text())

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
            # if event is json serializable, append it to logs.log file
            try:
                with open("logs.log", "a") as f:
                    print(event, file=f)

            except Exception as e:
                print(f"Error writing to logs.log: {e}")

            print(kind)
            if kind == "on_chat_model_stream":
                bot_messages_by_id[event["run_id"]] = (
                    bot_messages_by_id.get(event["run_id"], "")
                    + event["data"].get("chunk", None).content  # type: ignore
                )

                print(
                    f"Chat model chunk: {repr(event['data'].get('chunk', None).content)}",  # type: ignore
                    flush=True,
                )
                event_data: AIMessageChunk = event["data"].get("chunk", None)  # type: ignore
                if (
                    event_data.response_metadata
                    and bot_messages_by_id[event["run_id"]] != ""
                ):
                    session.add(
                        Message(
                            id=event_data.id,
                            content=bot_messages_by_id[event["run_id"]],
                            thread_id=thread_id,
                            sent_by=SentBy.bot,
                        )
                    )
                await websocket.send_json(
                    {
                        **event_data.dict(),
                        "metadata": event.get("metadata", {}),
                        "kind": event["event"],
                        "run_id": event["run_id"],
                        "name": event["name"],
                    }
                )

            if kind == "on_tool_start":
                print(f"Tool start: {event}", flush=True)

            if kind == "on_tool_end":
                print(f"Tool end: {event}", flush=True)

        session.commit()
