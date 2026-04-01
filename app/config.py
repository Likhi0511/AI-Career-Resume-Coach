import os
from dotenv import load_dotenv

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME", "rag-project-index")

DATABASE_URL = "postgresql+psycopg2://postgres:likhi1105@localhost:5432/rag_db"
