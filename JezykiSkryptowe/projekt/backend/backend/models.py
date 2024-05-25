from datetime import datetime
import enum
from uuid import uuid4
from sqlmodel import Field, Relationship, SQLModel


class ThreadBase(SQLModel):
    title: str
    created_at: datetime = Field(default_factory=datetime.now)


class Thread(ThreadBase, table=True):
    id: str | None = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    messages: list["Message"] = Relationship(back_populates="thread")


class ThreadPublic(ThreadBase):
    id: str


class ThreadPublicWithMessages(ThreadPublic):
    id: str
    messages: list["MessagePublic"]


class SentBy(str, enum.Enum):
    user = "user"
    bot = "bot"


class MessageKind(str, enum.Enum):
    message = "message"
    tool_start = "tool_start"
    tool_output = "tool_output"


class MessageBase(SQLModel):
    content: str
    sent_by: SentBy = Field(default=SentBy.user, nullable=False)
    kind: MessageKind = Field(default=MessageKind.message, nullable=False)
    tool_name: str | None = None


class Message(MessageBase, table=True):
    id: str | None = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    thread_id: str | None = Field(default=None, foreign_key="thread.id", nullable=False)
    thread: Thread | None = Relationship(back_populates="messages")


class MessagePublic(MessageBase):
    id: str
    thread_id: str


class FileBase(SQLModel):
    filename: str
    on_disk: str
    size: int


class File(FileBase, table=True):
    id: str | None = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class FilePublic(FileBase):
    id: str
    created_at: datetime


class MessageStore(SQLModel, table=True):
    __tablename__ = "message_store"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    session_id: str | None = Field(default=None)
    message: str | None = Field(default=None)
