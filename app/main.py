from app.routers.embedding import router as embedding_router
from app.routers.qdrant import router as qdrant_router
from app.routers.ui import router as ui_router
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

# Define app lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    #qdrant_svc.create_collection_default()
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
app.include_router(qdrant_router)
app.include_router(embedding_router)
app.include_router(ui_router)

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

