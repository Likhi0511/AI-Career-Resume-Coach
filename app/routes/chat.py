from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from ingestion.loader import pdf_load
from ingestion.chunking import split_doc
from ingestion.indexing import store_chunks

from app.services.rag_service import get_vectorstore, get_rag_chain
from app.db.memory import save_message, get_history

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default_session"


@router.post("/index")
async def index_pdf(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    docs = pdf_load(file_path)
    chunks = split_doc(docs)

    store_chunks(chunks)

    return {"message": "Indexed", "chunks": len(chunks)}


@router.post("/ask")
def ask(request: QuestionRequest):

    save_message(request.session_id, "user", request.question)

    vectorstore = get_vectorstore()
    chain = get_rag_chain(vectorstore)

    response = chain.invoke({"query": request.question})

    answer = response.get("result", "").strip()

    save_message(request.session_id, "assistant", answer)

    return {"answer": answer}
