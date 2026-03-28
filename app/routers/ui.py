from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/ui", tags=["Front-End"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/home")
def r_home(
            request: Request
        ):
    try:
        return templates.TemplateResponse(
            request=request,
            name='index.html',
            context={}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))