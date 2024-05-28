from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from backend.agents.rag import retrieval_tool
from langchain_community.tools.tavily_search import TavilySearchResults

from backend.core.config import settings


model = ChatOpenAI(model=settings.BASE_MODEL)
instructions = """Jesteś asystentem do zadań związanych z odpowiadaniem na pytania. Użyj fragmentów kontekstu lub bazy wiedzy, w skrajnych przypadkach użyj wyszukiwarki, aby odpowiedzieć na pytanie. Jeśli nie znasz odpowiedzi, po prostu powiedz, że nie wiesz. Utrzymaj odpowiedź zwięzłą.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [
    retrieval_tool,
    TavilySearchResults(
        name="google_search",
        description=(
            "Wyszukiwarka zoptymalizowana pod kątem kompleksowych, dokładnych i wiarygodnych wyników. "
            "Dane wejściowe powinny być zapytaniem wyszukiwania."
        ),
    ),
]

agent = create_openai_functions_agent(
    ChatOpenAI(temperature=0),
    tools,
    prompt,
)

agent_executor = AgentExecutor(
    agent=agent,  # type: ignore
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
)


with_message_history = RunnableWithMessageHistory(
    agent_executor,  # type: ignore
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string=settings.SQLITE_DATABASE_URI
    ),
    input_messages_key="question",
    history_messages_key="history",
)


def parse_message_with_stream(new_message: str, session_id: str):
    return with_message_history.astream_events(
        {
            "question": new_message,
        },
        version="v2",
        config=RunnableConfig(configurable={"session_id": session_id}),
    )
