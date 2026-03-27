from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client import QdrantClient
import uuid
# Modules
from app.services.embedding import EmbeddingService
from app.schemas.embedding import TextEmbedRequest
from app.core.config import settings

class QdrantService:
    def __init__(self, host:str, port:int, embedding_svc: EmbeddingService):
        self.client = QdrantClient(host=host, port=port)
        self.default_collection_name = "notes"
        self.embedding_svc = embedding_svc

    def create_collections(self, args_collection_names:list) -> None:
        # Get all collections in Qdrant currently
        collections = self.client.get_collections().collections
        c_names = [c.name for c in collections]
        # Check if given collection names exist, if not create
        for col in args_collection_names:
            if col not in c_names:
                self.client.create_collection(
                    collection_name=col,
                    vectors_config=VectorParams(size=4, distance=Distance.COSINE)
                )
    
    def create_collection_default(self) -> None:
            # Get all collections in Qdrant currently
            collections = self.client.get_collections().collections
            c_names = [c.name for c in collections]
            # Check if given collection name exist, if not create
            if self.default_collection_name not in c_names:
                self.client.create_collection(
                    collection_name=self.default_collection_name,
                    vectors_config=VectorParams(
                        size=settings.qdrant_vector_length,
                        distance=Distance.COSINE #COSINE DOT EUCLID MANHATTAN
                    )
                )
            return {"message": "ok"}

    def get_collection_info(self) -> list[dict]:
        collections = self.client.get_collections().collections
        result = []
        for collection in collections:
            info = self.client.get_collection(collection.name)

            result.append({
                "name": collection.name,
                "vector_size": info.config.params.vectors.size,
                "distance": str(info.config.params.vectors.distance),
                "points_count": info.points_count,
            })
        return result

    def store_vector(self, payload: TextEmbedRequest) -> dict:
        emb_resp = self.embedding_svc.embed_text(payload=payload)
        if emb_resp.get('vector_size') != settings.qdrant_vector_length:
            err_str= '\n'.join([
                "Embedded vector length does not match qdrant collection's vector length",
                f"emb len:{emb_resp.get('vector_size')}",
                f"val_type:{type(emb_resp.get('vector_size'))}",
                f"qdrant len:{settings.qdrant_vector_length}",
                f"val_type:{type(settings.qdrant_vector_length)}",
            ])
            raise ValueError(err_str)
        vector = emb_resp.get("vector")
        # Check if generated point_id already exists
        for _ in range(5):
            point_id = str(uuid.uuid4())
            existing = self.client.retrieve(
                    collection_name=self.default_collection_name,
                    ids=[point_id],
                )
            if not existing:
                break
        else:
            raise ValueError("Failed to generate a unique point id, try again")
        # Insert vector
        self.client.upsert(
            collection_name = self.default_collection_name,
            points = [
                PointStruct(
                    id = point_id,
                    vector = vector,
                    payload={"text":payload.text}
                )
            ]
        )
        return {"point_id": point_id}
