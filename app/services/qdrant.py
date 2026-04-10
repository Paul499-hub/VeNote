from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import PointIdsList
from qdrant_client import QdrantClient
import uuid
# Modules
from app.schemas.embedding import IN_TextEmbedRequest, F_EmbedTextOut, IN_SimilaritySearchRequest
from app.services.embedding import EmbeddingService
from app.core.helpers import parse_into_markdown
from app.services.sqlite import SQLiteService
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

    def validate_emb_response_len(self, emb_resp: F_EmbedTextOut):
        if emb_resp.vector_size != settings.qdrant_vector_length:
            raise ValueError(
                f"Embedded vector len does not match qdrant collection's vector length",
                f"emb len: {emb_resp.vector_size}",
                f"qdrant len: {settings.qdrant_vector_length}"
            )

    def embed_text(self, text:str) -> F_EmbedTextOut:
        # E5 models were trained with "passage/query" prefixes
        text_to_embed = text
        if settings.embedding_model == "intfloat/e5-large-v2":
            text_to_embed = f"passage: {text_to_embed}"
        emb_resp:F_EmbedTextOut = self.embedding_svc.embed_text(text=text_to_embed)
        self.validate_emb_response_len(emb_resp)
        return emb_resp, text_to_embed

    def store_vector(self, text:str, note_id:int) -> dict:
        emb, text_to_embed = self.embed_text(text)
        vector = emb.vector
        # Insert vector
        self.client.upsert(
            collection_name = self.default_collection_name,
            points = [
                PointStruct(
                    id = note_id,
                    vector = vector,
                    payload={"text":text}
                )
            ]
        )
        return {"point_id": note_id, "text_to_embed":text_to_embed}

    def similarity_search(self, payload: IN_SimilaritySearchRequest, args_limit:int = 5):
        # E5 models were trained with "passage/query" prefixes
        text_to_embed = payload.text
        if settings.embedding_model == "intfloat/e5-large-v2":
            text_to_embed = f"query: {text_to_embed}"
        emb_resp:F_EmbedTextOut = self.embedding_svc.embed_text(text=text_to_embed)
        self.validate_emb_response_len(emb_resp)
        vector = emb_resp.vector
        search_result = self.client.query_points(
            collection_name = self.default_collection_name,
            query = vector,
            limit = args_limit,
        )
        return [
            {
                "id": s.id,
                "score": s.score,
                "text":  s.payload.get("text") if s.payload else None,
                "html_md": parse_into_markdown(s.payload.get('text')) if s.payload else None, 
                "text_to_embed": text_to_embed,
            }
            for s in search_result.points
        ]
    
    def delete_vector(self, note_id:int) -> dict:
        self.client.delete(
            collection_name = self.default_collection_name,
            points_selector = PointIdsList(points=[note_id]),
        )
        return {"deleted_point_id": note_id}
        