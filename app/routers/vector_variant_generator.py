from fastapi import APIRouter
# Modules
from app.core.services import vector_variant_svc
from app.schemas.ai import AiInput

router = APIRouter(prefix="/vector_variant_generator", tags=["vector_variant_generator"])

@router.post("/send_msg_to_ai", status_code=200)
def r_msg(
        payload: AiInput
        ):
    try:
        return vector_variant_svc.msg_ai(msg=payload.msg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))