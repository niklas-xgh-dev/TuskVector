from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .api_key_service import router as api_key_service
from .items_router import router as items_router
from .embeddings_router import router as embeddings_router
from .llm_router import router as llm_router
from .database import create_tables
import os

create_tables()

app = FastAPI(docs_url="/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tuskvector.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, prefix="/api")
app.include_router(embeddings_router, prefix="/api")
app.include_router(llm_router, prefix="/api")
app.include_router(api_key_service, prefix="/api")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

app.mount("/", StaticFiles(directory=project_root), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse(os.path.join(project_root, 'index.html'))