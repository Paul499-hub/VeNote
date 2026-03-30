from fastapi import APIRouter, HTTPException
# Modules
from app.core.services import sqlite_svc
from app.schemas.embedding import IN_TextEmbedRequest

router = APIRouter(prefix="/sqlite", tags=["Sqlite"])

@router.post("/save", status_code=200)
def r_save_note_sqlite(
                    payload: IN_TextEmbedRequest
                    ):
    try:
        return sqlite_svc.create_note(payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/get", status_code=200)
def r_find_note_sqlite(
                    payload: IN_TextEmbedRequest
                    ):
    try:
        return sqlite_svc.find_note_contains(text=payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/del/{note_id}", status_code = 201)
def r_delete_note_sqlite(
                        note_id: int
                        ):
    try:
        return sqlite_svc.delete_note(note_id = note_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/count_notes", status_code=200)
def r_count_notes():
    try:
        return sqlite_svc.count_notes()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
