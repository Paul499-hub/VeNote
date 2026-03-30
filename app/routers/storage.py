from fastapi import APIRouter, HTTPException
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