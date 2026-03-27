from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

class QdrantService:
    def __init__(self, host:str, port:int):
        self.client = QdrantClient(host=host, port=port)
        
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
    
    def get_collection_names(self) -> list[str]:
        collections = self.client.get_collections().collections
        return [c.name for c in collections]
