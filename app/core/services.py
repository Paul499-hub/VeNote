from app.services.embedding import EmbeddingService
from app.services.qdrant import QdrantService
from app.core.config import settings

embedding_svc = EmbeddingService()
qdrant_svc = QdrantService(
    embedding_svc=embedding_svc,
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)
