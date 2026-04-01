
# 🚀 AI Career & Resume Coach

An intelligent **Conversational RAG (Retrieval-Augmented Generation)** system that analyzes resumes, identifies skill gaps, and provides personalized career guidance using LLMs.

---

## 🎯 Overview

This project allows users to:

- Upload resumes (PDF)
- Ask questions about their profile
- Identify missing skills
- Get improvement suggestions
- Receive career guidance

It combines **RAG + LLM + Memory** to deliver contextual and conversational responses.

---

## Architecture Diagram
                ┌────────────────────┐
                │   Streamlit UI     │
                │  (User Interface)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   FastAPI Backend  │
                │   (API Layer)      │
                └─────────┬──────────┘
                          │
          ┌───────────────┼────────────────┐
          ▼                                ▼
┌────────────────────┐         ┌────────────────────┐
│   RAG Pipeline     │         │   Chat Memory      │
│   (LangChain)      │         │   (PostgreSQL)     │
└─────────┬──────────┘         └────────────────────┘
          │
          ▼
┌────────────────────┐
│   Vector Database  │
│   (Pinecone)       │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│      OpenAI LLM    │
│ (GPT-4o / mini)    │
└────────────────────┘
This architecture enables a hybrid AI system combining Retrieval-Augmented Generation (RAG) with conversational memory.

## 🧠 Key Features

- 📄 Resume Analysis using RAG
- 💬 Conversational Chat Interface (Streamlit)
- 🧠 Hybrid AI (RAG + LLM fallback)
- 🗂 Vector Search using Pinecone
- 🧾 Chat Memory using PostgreSQL
- ⚡ FastAPI Backend
- 🎯 Domain-specific Career Guidance

---

## 🏗 Architecture

User (Streamlit UI)
↓
FastAPI Backend
↓
RAG Pipeline (LangChain)
↓
Pinecone (Vector DB) + PostgreSQL (Memory)
↓
OpenAI LLM

---

## 📁 Project Structure

career-coach-ai/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── config.py # Environment variables
│
│ ├── routes/
│ │ └── chat.py # API endpoints
│
│ ├── services/
│ │ └── rag_service.py # RAG pipeline logic
│
│ ├── db/
│ │ ├── postgres.py # DB connection
│ │ └── memory.py # Chat history
│
├── ingestion/
│ ├── loader.py # PDF loading
│ ├── chunking.py # Text splitting
│ └── indexing.py # Vector storage
│
├── ui/
│ └── chat_ui.py # Streamlit UI
│
├── .streamlit/
│ └── config.toml # UI theme
│
├── requirements.txt
├── .env
└── README.md


---

## ⚙️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: FastAPI  
- **LLM**: OpenAI (GPT models)  
- **Framework**: LangChain  
- **Vector DB**: Pinecone  
- **Database**: PostgreSQL  
- **Embeddings**: OpenAI Embeddings  

---

## 🔄 How It Works

1. User uploads a resume (PDF)
2. Document is:
   - Loaded → Cleaned → Chunked
3. Chunks are converted into embeddings
4. Stored in Pinecone vector database
5. User asks questions
6. System:
   - Retrieves relevant chunks (RAG)
   - Combines with LLM
   - Returns structured answer
7. Chat history is stored in PostgreSQL

---

## 🧪 Example Queries

- What skills are missing in my resume?
- Suggest improvements to my resume
- What roles can I apply for?
- How can I become an AI engineer?

---

## 🚀 Setup Instructions

### 
1. Clone Repository

```bash
git clone https://github.com/your-username/career-coach-ai.git
cd career-coach-ai

2. Install Dependencies
pip install -r requirements.txt
3. Set Environment Variables

Create a .env file:

OPENAI_API_KEY=your_key
PINECONE_API_KEY=your_key
INDEX_NAME=rag-project-index

4. Run Backend (FastAPI)
uvicorn app.main:app --reload

5. Run UI (Streamlit)
streamlit run ui/chat_ui.py
🎥 Demo
