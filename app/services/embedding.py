from app.schemas.embedding import IN_TextEmbedRequest, F_EmbedTextOut
from app.ai_models.model_registry import embedding_model
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        pass

    def embed_text(self, text:str) -> F_EmbedTextOut:
        vector = embedding_model.encode(text)
        return F_EmbedTextOut.model_validate({
            "status": "ok",
            "vector": vector.tolist(), # NumPy array -> list
            "vector_size": len(vector),
        })