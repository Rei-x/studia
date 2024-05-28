from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

instructions = """Jesteś ekspertem w tworzeniu małych i zwięzłych tytułów dla rozmów. Musisz stworzyć jednozdaniowy tytuł dla każdej wiadomości w rozmowie. Opisz to co otrzymałeś. Przykład:

Wiadomość: Cześć, jak się masz?
Twoja odpowiedź: Przyjazne powitanie.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{question}"),
    ]
)

title_generator = prompt | model | StrOutputParser()


def generate_title(message: str) -> str:
    return title_generator.invoke(input={"question": message})
