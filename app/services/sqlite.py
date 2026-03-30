from app.db.db import SessionLocal
from app.db.models import NoteORM

class SQLiteService():
    def create_note(self, text:str) -> NoteORM:
        session = SessionLocal()
        try:
            note = NoteORM(text=text)
            session.add(note)
            session.commit()
            session.refresh(note)
            return note
        finally:
            session.close()
    
    def find_note_contains(self, text:str) -> list[NoteORM]:
        session = SessionLocal()
        try:
            search_result = session.query(NoteORM).filter(NoteORM.text.contains(text)).all()
            return [
                {
                    "id": s.id,
                    "score": 1.0,
                    "text": s.text,
                }
                for s in search_result
            ]
        finally:
            session.close()
    
    def count_notes(self) -> int:
        session = SessionLocal()
        try:
            return session.query(NoteORM).count()
        finally:
            session.close()