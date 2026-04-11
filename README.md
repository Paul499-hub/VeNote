<img width="705" height="937" alt="image" src="https://github.com/user-attachments/assets/66f4114a-c9f8-4a66-9cf8-8d6628ee97dd" />




# 🚀 How to launch the project
1. Make sure Docker is installed and running.
2. Open a terminal in the project root directory (where `Dockerfile` and `docker-compose.yml` are).
3. Run `docker compose build`.
4. Run `docker compose up`.
5. Open `http://127.0.0.1:48721/ui/home` in your browser.

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
