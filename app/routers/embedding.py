from fastapi import APIRouter, HTTPException, Form
# Modules
from app.services.embedding import EmbeddingService
from app.schemas.embedding import TextEmbedRequest
from app.core.services import embedding_svc

router = APIRouter(prefix="/embed", tags=["Embedding"])

@router.post("/embed_text", status_code=200)
def embed_text(
                payload: TextEmbedRequest
            ):
    try:
        return embedding_svc.embed_text(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
