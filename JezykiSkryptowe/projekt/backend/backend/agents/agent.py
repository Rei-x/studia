from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from backend.agents.rag import retrieval_tool
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()


model = ChatOpenAI(model="gpt-3.5-turbo")
instructions = """Jesteś asystentem do zadań związanych z odpowiadaniem na pytania. Użyj fragmentów kontekstu lub bazy wiedzy, w skrajnych przypadkach użyj wyszukiwarki, aby odpowiedzieć na pytanie. Jeśli nie znasz odpowiedzi, po prostu powiedz, że nie wiesz. Użyj maksymalnie trzech zdań i utrzymaj odpowiedź zwięzłą.
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
    # PythonREPLTool(
    #     name="Python_script_runner",
    #     description="Użyj tego narzędzia do uruchamiania kodu Pythona i zawsze dodawaj instrukcję print, aby zobaczyć wynik.",
    # ),
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
    ChatOpenAI(temperature=0, name="Main-Model"),
    tools,
    prompt,
)

agent_executor = AgentExecutor(
    agent=agent,  # type: ignore
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,  # type: ignore
)


with_message_history = RunnableWithMessageHistory(
    agent_executor,  # type: ignore
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///db.sqlite3"
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
