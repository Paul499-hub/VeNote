from fastapi import APIRouter, HTTPException
# Modules
from app.schemas.embedding import TextEmbedRequest
from app.core.services import qdrant_svc

router = APIRouter(prefix="/qdrant", tags=["QDRANT"])

@router.get("/get_collections", status_code=200)
def qdrant_get_collection():
    try:
        return {"collections": qdrant_svc.get_collection_info()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_collections", status_code=200)
def qdrant_create_collections():
    try:
        qdrant_svc.create_collections(["notes_test"])
        return {"status": "ok", "collections": qdrant_svc.get_collection_info()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_collection_default", status_code=200)
def qdrant_create_collection():
    try:
        return qdrant_svc.create_collection_default()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store_note", status_code=200)
def store_note_in_qdrant(
                            payload: TextEmbedRequest
                        ):
    try:
        return qdrant_svc.store_vector(payload=payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
