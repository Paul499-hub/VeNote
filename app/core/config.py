import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.qdrant_host:str = os.getenv("QDRANT_HOST")
        self.qdrant_port:int = int(os.getenv("QDRANT_PORT"))
        self.embedding_model:str = os.getenv("EMBEDDING_MODEL")
        self.qdrant_vector_length:int = int(os.getenv("QDRANT_VECTOR_LENGTH"))

settings = Settings()
