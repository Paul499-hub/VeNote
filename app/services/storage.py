from app.services.qdrant import QdrantService
from app.services.sqlite import SQLiteService
from app.db.models import NoteORM
from app.db.db import SessionLocal
from sqlalchemy import select
from typing import List

class StorageService:
    """## Abstract service, using `qdrant` + `sqlite` storage functionalities"""
    def __init__(self, qdrant_svc: QdrantService, sqlite_svc: SQLiteService ):
        self.qdrant_svc = qdrant_svc
        self.sqlite_svc = sqlite_svc

    def save_note(self, text:str):
        sqlite_saved_note:NoteORM = self.sqlite_svc.create_note(text=text)
        note_id:int = sqlite_saved_note.id
        return self.qdrant_svc.store_vector(text=text,note_id=note_id)
        
    def del_note(self, note_id: int):
        self.qdrant_svc.delete_vector(note_id=note_id)
        return self.sqlite_svc.delete_note(note_id=note_id)
    
    def recreate_sqlite(self):
        session = SessionLocal()
        try:
            stmt = select(NoteORM.id, NoteORM.text)
            note_info = session.execute(stmt).yield_per(100)
            for note_id, text in note_info:
                self.qdrant_svc.store_vector(text=text, note_id=note_id)
            return {"message":"ok"}
        finally:
            session.close()

    def update_note(self, note_id:int, text:str):
        resp_sql = self.sqlite_svc.update_note(note_id, text)
        resp_qdrant = self.qdrant_svc.store_vector(text,note_id)
        return {"sqlite":resp_sql, "qdrant":resp_qdrant}
    