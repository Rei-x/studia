import tempfile
from typing import List
from langchain.callbacks import StdOutCallbackHandler
from pathlib import Path
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai.chat_models import ChatOpenAI as OpenAIChat
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter

import streamlit as st

from streaming import StreamHandler


TMP_DIR = Path(__file__).resolve().parent.joinpath("data", "tmp")
LOCAL_VECTOR_STORE_DIR = (
    Path(__file__).resolve().parent.joinpath("data", "vector_store")
)

vector_db = Chroma(
    persist_directory=LOCAL_VECTOR_STORE_DIR.as_posix(),
    embedding_function=OpenAIEmbeddings(api_key=st.secrets.openai_api_key),
)

st.set_page_config(page_title="RAG")
st.title("Retrieval Augmented Generation Engine")


if not st.secrets.openai_api_key:
    st.warning("Please add your OpenAI API key to the secrets.toml file.")

os.environ["OPENAI_API_KEY"] = st.secrets.openai_api_key


def load_documents():
    loader = PyPDFDirectoryLoader(TMP_DIR.as_posix(), glob="**/*.pdf")
    documents = loader.load()
    return documents


def split_documents(documents: List[Document]):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    return texts


def add_embeddings(texts: List[Document]):
    vector_db.add_documents(texts)
    vector_db.persist()


def input_fields():
    with st.sidebar:
        if "openai_api_key" in st.secrets:
            st.session_state.openai_api_key = st.secrets.openai_api_key
        else:
            st.session_state.openai_api_key = st.text_input(
                "OpenAI API key", type="password"
            )

    st.session_state.source_docs = st.file_uploader(
        label="Dodaj dokumenty",
        type="pdf",
        accept_multiple_files=True,
    )


def process_documents():
    if not st.session_state.openai_api_key or not st.session_state.source_docs:
        st.warning("Dodaj dokumenty!")
    else:
        try:
            if not TMP_DIR.exists():
                TMP_DIR.mkdir(parents=True)
            for source_doc in st.session_state.source_docs:
                with tempfile.NamedTemporaryFile(
                    delete=False, dir=TMP_DIR.as_posix(), suffix=".pdf"
                ) as tmp_file:
                    tmp_file.write(source_doc.read())

            documents = load_documents()
            texts = split_documents(documents)
            add_embeddings(texts)
            st.toast("Dokumenty dodane!")

        except Exception as e:
            st.error(f"An error occurred: {e}")


def boot():
    input_fields()
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    st.session_state.retriever = retriever
    st.button(
        "Dodaj dokumenty",
        on_click=process_documents,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.chat_message("assistant").write("Witaj w RAG!")
    for msg in st.session_state.messages:
        st.chat_message("user").write(msg[0])
        st.chat_message("assistant").write(msg[1])

    if query := st.chat_input("Zadaj pytanie!"):
        st.chat_message("user").write(query)

        with st.spinner("Thinking..."):
            with st.chat_message("assistant"):
                message = st.empty()

                question_prompt = PromptTemplate.from_template(
                    (
                        "Połącz historię rozmowy z pytaniem, aby uzyskać odpowiedź na "
                        "zadane pytanie. Twoja odpowiedź zostanie wysłana do bazy wektorowej. Historia czatu: {chat_history} \n"
                        "Pytanie: {question}"
                    )
                )
                answer_prompt = PromptTemplate.from_template(
                    """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Always answer in users language. Use markdown formatting.

Chat history: {chat_history}

Question: {question} 

Context: {context} 

Answer:"""
                )
                stream_handler = StreamHandler(message)
                qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=OpenAIChat(
                        api_key=st.session_state.openai_api_key,
                        streaming=True,
                        callbacks=[stream_handler],
                        model="gpt-4-turbo-preview",
                    ),
                    rephrase_question=False,
                    callbacks=[StdOutCallbackHandler()],
                    condense_question_prompt=question_prompt,
                    combine_docs_chain_kwargs={
                        "prompt": answer_prompt,
                    },
                    condense_question_llm=OpenAIChat(
                        api_key=st.session_state.openai_api_key,
                    ),
                    retriever=retriever,
                    return_source_documents=True,
                )

                response = qa_chain(
                    {"question": query, "chat_history": st.session_state.messages},
                )

                docs: List[Document] = response["source_documents"]

                for idx, doc in enumerate(docs):
                    with st.expander(f"Source nr {str(idx + 1)}"):
                        st.write(doc.page_content)
                st.session_state.messages.append((query, response["answer"]))
                message.markdown(response["answer"])


if __name__ == "__main__":
    boot()
