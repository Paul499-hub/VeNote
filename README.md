<img width="1279" height="840" alt="image" src="https://github.com/user-attachments/assets/9f9e64d2-fd16-485d-99fc-ae5d4b59703e" />

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
- Default: `text-embedding-3-small` (fast & accurate)
- Optional: local `sentence-transformers` for offline mode

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


## For local runs 
uv sync 
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
