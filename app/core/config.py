import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
ROOT_DIR = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parents[1]

class Settings:
    def __init__(self):
        self.qdrant_host:str = os.getenv("QDRANT_HOST")
        self.qdrant_port:int = int(os.getenv("QDRANT_PORT"))
        self.embedding_model:str = os.getenv("EMBEDDING_MODEL")
        self.qdrant_vector_length:int = int(os.getenv("QDRANT_VECTOR_LENGTH"))
        self.sqlite_db_path:str =os.getenv("SQLITE_DB_PATH") 

settings = Settings()
