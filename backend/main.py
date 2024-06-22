from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from items_router import router as items_router
from database import create_tables

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