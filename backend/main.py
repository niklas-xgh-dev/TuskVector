from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from items_router import router as items_router
from database import create_tables
import os

create_tables()

app = FastAPI(docs_url="/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gorillavector.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, prefix="/api")

app.include_router(items_router, prefix="/api")

# Get the directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(current_dir)

# Serve static files from the project root
app.mount("/", StaticFiles(directory=project_root), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse(os.path.join(project_root, 'index.html'))