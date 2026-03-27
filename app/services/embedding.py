from sentence_transformers import SentenceTransformer
from app.schemas.embedding import TextEmbedRequest
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed_text(self, payload: TextEmbedRequest) -> dict:
        vector = self.model.encode(payload.text)
        return {
            "status": "ok",
            "vector": vector.tolist(), # NumPy array -> list
            "vector_size": len(vector),
        }