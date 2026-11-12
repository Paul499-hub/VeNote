from app.services.qdrant import QdrantService
from app.services.sqlite import SQLiteService
from app.db.models import NoteORM
from app.db.db import SessionLocal
from sqlalchemy import select
from typing import List
# Modules
from app.schemas.embedding import IN_TextEmbedRequest, F_EmbedTextOut, IN_SimilaritySearchRequest
from app.core.helpers import parse_into_markdown

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
    
    def recreate_from_sqlite(self):
        """Re build all Qdrant points from SQLite source"""
        session = SessionLocal()
        try:
            self.qdrant_svc.clear_points()
            stmt = select(NoteORM.id, NoteORM.text)
            note_info = session.execute(stmt).yield_per(100)
            for note_id, text in note_info:
                self.qdrant_svc.store_vector(text=text, note_id=note_id)
            return {"message":"ok"}
        finally:
            session.close()

    def update_note(self, note_id: int, text: str):
        self.sqlite_svc.update_note(note_id, text)
        self.qdrant_svc.delete_vector(note_id)
        self.qdrant_svc.store_vector(text, note_id)
        return {"message": "ok"}

    def vector_search_note(self, payload: IN_SimilaritySearchRequest):
        vector_points: list[dict] = self.qdrant_svc.similarity_search(payload) # Returned vector search points
        # Many vector retrieved points can share same sqlite_id
        # Find highest score for each matching sqlite_id 
        memory: dict[int, float] = {} # Key = sqlite_id: int , value = score: float 
        for vp in vector_points:
            sid, score = int(vp["sqlite_id"]), vp["score"]
            if sid in memory:
                memory[sid] = max(memory[sid], score)
            else:
                memory[sid] = score
        sqlite_ids = memory.keys()
        # Find actual note text from SQLite 
        note_orms: list[NoteORM] = self.sqlite_svc.find_notes_by_ids(ids = sqlite_ids)
        return [
            {
                "id": n.id,
                "score": memory[n.id],
                "text": n.text,
                "html_md" : parse_into_markdown(n.text),
            }
            for n in sorted(note_orms, key=lambda note: memory[note.id], reverse=True)
        ]

    