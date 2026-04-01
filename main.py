import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:likhi1105@localhost:5432/rag_db"

engine = create_engine(DATABASE_URL)

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME","rag-project-index")

app = FastAPI(title="RAG API with LangChain")

pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine"
    )
    print(pc.list_indexes())
    index = pc.Index(INDEX_NAME)
    print(index.describe_index_stats())


def create_table():
    with engine.begin() as conn:   # ✅ IMPORTANT
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

create_table()


def save_message(session_id, role, message):
    with engine.begin() as conn:
        conn.execute(text("""
                INSERT INTO chat_history (session_id, role, message)
                VALUES (:session_id, :role, :message)
            """), {
                "session_id": session_id,
                "role": role,
                "message": message
            })
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an AI Career Coach.

Use the provided context to answer the question.

Rules:
- Answer based on the context as much as possible
- If partial information is available, answer using that
- Only say "I don't know" if absolutely no relevant info exists

Keep answers:
- Clear
- Concise (max 100 words)

Context:
{context}

Question:
{question}

Answer:
"""
)
def pdf_load(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 🔥 CLEAN TEXT
    for doc in docs:
        text = doc.page_content

        # remove weird spacing
        text = text.replace("\n", " ")
        text = " ".join(text.split())

        doc.page_content = text

    return docs

def split_doc(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
    )
    return splitter.split_documents(documents)

def vector_store(chunks):
    embeddings = OpenAIEmbeddings()

    filtered_chunks = []

    for chunk in chunks:
        text = chunk.page_content.lower()

        # ✅ Keep only useful resume content
        if any(keyword in text for keyword in [
            "experience", "skills", "project", "profile", "education"
        ]):
            filtered_chunks.append(chunk)

    print(f"Filtered chunks: {len(filtered_chunks)}")

    vectorstore = PineconeVectorStore.from_documents(
        documents=filtered_chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    return vectorstore

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return PineconeVectorStore.from_existing_index(
        INDEX_NAME,
        embeddings

        )

def rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    llm = ChatOpenAI(model="gpt-4o-mini")
    qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return qa_chain

def get_history(session_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT role, message FROM chat_history
            WHERE session_id = :session_id
            ORDER BY created_at
        """), {"session_id": session_id})

        return result.fetchall()

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default_session"

@app.post("/index")
async def index_pdf(file: UploadFile = File(...)):

    try:
        print("Uploading file...")

        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        print("File saved:", file_path)

        docs = pdf_load(file_path)
        print("PDF loaded")

        chunks = split_doc(docs)
        print("Chunks created:", len(chunks))

        print("\n--- SAMPLE CHUNK ---")
        print(chunks[0].page_content[:300])

        index = pc.Index(INDEX_NAME)
        print("Deleting old vectors...")
        index.delete(delete_all=True)
        print("Index cleared")

        vector_store(chunks)
        print("Stored in Pinecone")

        return {
            "message": "PDF indexed successfully",
            "chunks": len(chunks)
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}

@app.post("/ask")
def ask_question(request: QuestionRequest):


    try:
        session_id = request.session_id

        # Save user message
        save_message(session_id, "user", request.question)

        # Get history
        history = get_history(session_id)[-5:]

        history_text = "\n".join(
            [f"{row[0]}: {row[1]}" for row in history]
        )

        # Get vectorstore + chain
        vectorstore = get_vectorstore()

        retriever = vectorstore.as_retriever(search_kwargs={"k":3})

        docs = retriever.get_relevant_documents(request.question)

        print("\n--- RETRIEVED DOCS ---")
        for i, d in enumerate(docs):
            print(f"\nDoc {i + 1}:\n", d.page_content[:200])

        qa_chain = rag_chain(vectorstore)

        # Combine history + question
        full_query = f"""
        Answer ONLY from resume details like skills, experience, projects.

        Question: {request.question}
        """
        response = qa_chain.invoke({
            "query": full_query
        })
        docs = response.get("source_documents", [])
        print("\n--- Retrieved Docs ---")
        for i, doc in enumerate(docs):
            print(f"\nDoc {i + 1}:\n", doc.page_content[:300])

        answer = response.get("result") or response.get("answer") or str(response)
        answer = answer.strip()

        # Limit length (optional safety)
        if len(answer.split()) > 120:
            answer = " ".join(answer.split()[:120]) + "..."

        print("Saving message to DB...")
        save_message(session_id, "assistant", answer)


        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}

    print("\n--- FINAL CONTEXT SENT TO LLM ---")
    print(response)


