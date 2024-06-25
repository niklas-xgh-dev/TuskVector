from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

class ApiKeyDB(Base):
    __tablename__ = "apikeys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    source_ip = Column(String(45), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True))

class TextEmbedding(Base):
    __tablename__ = "text_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db)):
    if api_key is None:
        raise HTTPException(status_code=401, detail="API Key is missing")
    
    api_key_db = db.query(ApiKeyDB).filter(ApiKeyDB.key == api_key).first()
    if api_key_db is None:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    api_key_db.last_used_at = datetime.utcnow()
    db.commit()
    
    return api_key