
from app.services.vector_variant_generator import VectorVariantGeneratorService
from app.services.embedding import EmbeddingService
from app.services.storage import StorageService
from app.services.sqlite import SQLiteService
from app.services.qdrant import QdrantService
from app.core.config import settings

embedding_svc = EmbeddingService()
sqlite_svc = SQLiteService()
qdrant_svc = QdrantService(
    embedding_svc=embedding_svc,
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)
storage_svc = StorageService(
    qdrant_svc=qdrant_svc,
    sqlite_svc=sqlite_svc
)
vector_variant_svc = VectorVariantGeneratorService()
