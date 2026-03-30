from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import logging
# Modules
from app.routers.embedding import router as embedding_router
from app.routers.storage import router as storage_router
from app.routers.qdrant import router as qdrant_router
from app.routers.sqlite import router as sqlite_router
from app.routers.ui import router as ui_router
from app.core.config import ROOT_DIR, APP_DIR
from app.core.services import qdrant_svc
from app.db.db import Base, engine

logger = logging.getLogger(__name__)

# Define app lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    qdrant_svc.create_collection_default() # Create note table in Qdrant
    Base.metadata.create_all(bind=engine)  # Create note table in SQLite
    logger.warning(f"ROOT_DIR --- {ROOT_DIR}")
    logger.warning(f"APP_DIR --- {APP_DIR}")
    yield
# Define app
app = FastAPI(lifespan=lifespan)
# Register css/js
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)
# Register routers
app.include_router(embedding_router)
app.include_router(storage_router)
app.include_router(qdrant_router)
app.include_router(sqlite_router)
app.include_router(ui_router)

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

