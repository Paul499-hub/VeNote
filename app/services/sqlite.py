from sqlalchemy import select
# Modules
from app.core.helpers import parse_into_markdown
from app.db.db import SessionLocal
from app.db.models import NoteORM
from app.schemas.note import Note

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
                    "html_md": parse_into_markdown(s.text), 
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

    def delete_note(self, note_id:int ):
        session = SessionLocal()
        try:
            note = session.get(NoteORM, note_id)
            if not note:
                raise ValueError(f"Note with id {note_id} not found")
            session.delete(note)
            session.commit()
            return {"deleted_note_id": note_id}
        finally:
            session.close()

    def deduplicate_sqlite(self):
        session = SessionLocal()
        try:
            stmt = select(NoteORM.id, NoteORM.text).order_by(NoteORM.id)
            notes = session.execute(stmt).yield_per(100)
            seen = set()
            duplicate_ids = []
            for note_id, text in notes:
                if text in seen:
                    duplicate_ids.append(note_id)
                else:
                    seen.add(text)
        finally:
            session.close()
        for note_id in duplicate_ids:
            self.delete_note(note_id)
        return {"message": "ok", "deleted_duplicates": len(duplicate_ids)}
    
    def update_note(self, note_id:int, text:str):
        session = SessionLocal()
        try:
            new_note:Note = Note.model_validate({"id": note_id, "text": text})
            old_note:NoteORM = session.get(NoteORM, note_id)
            if not old_note:
                raise ValueError("Note not found")
            old_text_cache = old_note.text
            old_note.text = new_note.text
            session.commit()
            session.refresh(old_note)
            return {"updated_id":f"{note_id}", "old_text":old_text_cache, "new_text":new_note.text}
        finally:
            session.close()