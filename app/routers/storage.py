from fastapi import APIRouter, HTTPException
# Modules
from app.schemas.embedding import IN_UpdateRequest
from app.core.services import storage_svc
from app.schemas.note import NoteCreate


router = APIRouter(prefix='/storage', tags=["Storage"])

@router.post("/save_note", status_code=200)
def r_save_note(
                payload: NoteCreate
            ):
    try:
        return storage_svc.save_note(text=payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/del/{note_id}")
def r_delete_note(
                note_id: int
                ):
    try:
        return storage_svc.del_note(note_id = note_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/recreate_from_sqlite_file", status_code=200)
def r_recreate_from_sqlite():
    try:
        return storage_svc.recreate_sqlite()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/update_note", status_code=200)
def r_update_note(
                payload: IN_UpdateRequest
            ):
    try:
        return storage_svc.update_note(note_id=payload.id, text=payload.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))