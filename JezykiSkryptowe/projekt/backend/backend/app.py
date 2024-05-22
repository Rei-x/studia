from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from backend.agent import parse_message_with_stream
from dotenv import load_dotenv

from backend.api.deps import SessionDep
from backend.models import (
    Message,
    MessagePublic,
    SentBy,
    Thread,
    ThreadPublicWithMessages,
)

load_dotenv()
app = FastAPI()


class ResponseModel(BaseModel):
    message: str


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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


@app.get("/", response_model=ResponseModel)
async def root():
    return {"message": "Hello World"}


@app.get("/messages", response_model=list[MessagePublic])
async def messages(session: SessionDep):
    messages = select(Message).limit(10)

    return session.exec(messages).all()


@app.get("/threads", response_model=list[ThreadPublicWithMessages])
async def threads(session: SessionDep):
    threads = select(Thread).limit(10)

    return session.exec(threads).all()


@app.websocket("/chat/{thread_id}")
async def chat_endpoint(websocket: WebSocket, session: SessionDep, thread_id: str):
    await websocket.accept()

    does_exist = session.exec(
        select(Thread).where(Thread.id == thread_id)
    ).one_or_none()

    while True:
        user_message = await websocket.receive_text()

        if not does_exist:
            thread = Thread(id=thread_id, title="Thread")
            session.add(thread)
            session.commit()

            does_exist = session.exec(
                select(Thread).where(Thread.id == thread_id)
            ).one_or_none()

        message_stream = parse_message_with_stream(user_message, thread_id)

        session.add(
            Message(content=user_message, thread_id=thread_id, sent_by=SentBy.user)
        )

        bot_message = ""
        async for message in message_stream:
            response = message.dict()

            if response.get("response_metadata", False):
                session.add(
                    Message(
                        content=bot_message, thread_id=thread_id, sent_by=SentBy.bot
                    )
                )

            bot_message += response.get("content", "")
            await websocket.send_json(response)

        session.commit()
