from app.routers.qdrant import router as qdrant_router
from fastapi import FastAPI
import uvicorn

# Define app
app = FastAPI()
# Register routers
app.include_router(qdrant_router)

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

