<img width="1275" height="777" alt="image" src="https://github.com/user-attachments/assets/c4202172-ab0f-4e2e-bcbc-e9c95207575d" />


# 📝 VectorNotepad: Project Architecture Overview

VectorNotepad is a local + docker AI-powered note storage and sematic search system.
Its goal is to store Markdown notes (text + images) and retrieve them using both **exact keyword search**
and *semantic meaning-based search* powered by vector embeddings.

---

# 🧱 Core Technologies

## 🐍 Backend: **FastAPI**
- note ingestion
- embedding generation
- vector database operations
- future API endpoints

## 🧬 Embeddings: **OpenAI or Local Models**
Used to transform note text into numerical vectors for similarity search.
- Default: local `sentence-transformers` for offline mode
- Future: `text-embedding-3-small` (fast & accurate)

## 🧩 Vector Database: **Qdrant**
Vector database used to store
- note text
- embeddings
- metadata (tags, timestamps, markdown flgs, etc.)

## 🐳 Containerization: **Docker + docker-compose**
The entire stack runs locally in isolated containers:
- Backend service (FastAPI)
- Qdrant vector database
- Optional UI container (future)
