# database.py
from sqlmodel import SQLModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    SQLModel.metadata.create_all(engine)
   # Call this function when your application starts
    if __name__ == "__main__":
        create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Item(SQLModel, table=True):
    __tablename__ = "item"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float