from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.config import INDEX_NAME

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a Career Coach AI.

Answer concisely (max 100 words).

Context:
{context}

Question:
{question}

Answer:
"""
)

def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    return PineconeVectorStore.from_existing_index(
        INDEX_NAME,
        embeddings
    )

def get_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini")

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
