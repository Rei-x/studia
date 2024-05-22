from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()


model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


chain = prompt | model
with_message_history = RunnableWithMessageHistory(
    chain,  # type: ignore
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///db2.sqlite3"
    ),
    input_messages_key="question",
    history_messages_key="history",
)


def parse_message_with_stream(new_message: str, session_id: str):
    return with_message_history.astream(
        {
            "question": new_message,
        },
        config=RunnableConfig(configurable={"session_id": session_id}),
    )
