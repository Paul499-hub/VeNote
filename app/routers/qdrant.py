from fastapi import APIRouter, HTTPException
# Modules
from app.services.qdrant import QdrantService
from app.core.config import settings


router = APIRouter(prefix="/qdrant", tags=["QDRANT"])
qdrant_svc = QdrantService(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

@router.get("/get_collections", status_code=200)
def qdrant_get_collection():
    try:
        return {"collections": qdrant_svc.get_collection_names()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_collections", status_code=200)
def qdrant_create_collection_test():
    try:
        qdrant_svc.create_collections(["notes_test"])
        return {"status": "ok", "collections": qdrant_svc.get_collection_names()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
