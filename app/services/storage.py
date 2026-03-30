from app.services.qdrant import QdrantService
from app.services.sqlite import SQLiteService
from app.db.models import NoteORM

class StorageService:
    """## Abstract service, using `qdrant` + `sqlite` storage functionalities"""
    def __init__(self, qdrant_svc: QdrantService, sqlite_svc: SQLiteService ):
        self.qdrant_svc = qdrant_svc
        self.sqlite_svc = sqlite_svc

    def save_note(self, text:str):
        sqlite_saved_note:NoteORM = self.sqlite_svc.create_note(text=text)
        note_id:int = sqlite_saved_note.id
        return self.qdrant_svc.store_vector(text=text,note_id=note_id)
        