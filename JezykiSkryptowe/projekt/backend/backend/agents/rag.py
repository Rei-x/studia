from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from langchain_community.document_loaders import UnstructuredAPIFileIOLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain_core.tools import Tool
from backend.core.config import settings
import io

from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model=settings.BASE_EMBEDDING)
qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

qdrant = Qdrant(qdrant_client, "docs", embeddings)


async def process_file_with_unstructured(file: bytes, filename: str, id: str):
    loader = UnstructuredAPIFileIOLoader(
        file=io.BytesIO(file),
        api_key=settings.UNSTRUCTURED_API_KEY,
        metadata_filename=filename,
    )
    splitter = RecursiveCharacterTextSplitter()

    docs_from_loader = await loader.aload()
    splitted_docs = await splitter.atransform_documents(docs_from_loader)

    for doc in splitted_docs:
        doc.metadata = {"filename": filename, "id": id}

    return await qdrant.aadd_documents(list(splitted_docs))


def search(query: str):
    result = qdrant.search(query, "similarity")

    return result


retrieval_tool = Tool(
    name="baza_wiedzy",
    description="Używaj tego narzędzia gdy chcesz wyszukać odpowiedzi na pytania",
    func=search,
)
