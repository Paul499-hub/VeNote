import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.qdrant_host=os.getenv("QDRANT_HOST")
        self.qdrant_port=os.getenv("QDRANT_PORT")

settings = Settings()
