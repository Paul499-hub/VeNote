from sentence_transformers import SentenceTransformer
from app.schemas.embedding import IN_TextEmbedRequest, F_EmbedTextOut
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model, trust_remote_code=True)

    def embed_text(self, text:str) -> F_EmbedTextOut:
        vector = self.model.encode(text)
        return F_EmbedTextOut.model_validate({
            "status": "ok",
            "vector": vector.tolist(), # NumPy array -> list
            "vector_size": len(vector),
        })