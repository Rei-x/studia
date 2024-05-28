# RAG with function calling

This is an example of using RAG with function calling. The backend is a FastAPI server that uses Qdrant to search for similar documents and OpenAI to generate the answer. Documents are processed with unstructured. The frontend is a NextJS app that allows the user to ask a question and get an answer.

## Pre-requisites

- Python 3.11
- Node.js 20
- Poetry

## Environment variables

- QDRANT_URL -> url of your qdrant instance
- QDRANT_API_KEY -> api key of your qdrant instance
- OPENAI_API_KEY -> api key to openai
- TAVILY_API_KEY -> api key to tavily
- UNSTRUCTURED_API_KEY -> api key to hosted unstructured

## How to run it?

```bash
cd backend
poetry install
fastapi dev backend
```

```bash
cd frontend
npm install
npm run dev
```
