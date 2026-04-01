from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.config import INDEX_NAME

def store_chunks(chunks):
    embeddings = OpenAIEmbeddings()

    filtered = [
        c for c in chunks
        if any(k in c.page_content.lower() for k in
               ["experience", "skills", "project", "education"])
    ]

    return PineconeVectorStore.from_documents(
        documents=filtered,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
