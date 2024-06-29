from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True

class TextEmbeddingCreate(BaseModel):
    text: str

class TextEmbeddingResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True

class SimilaritySearchRequest(BaseModel):
    text: str

class SimilaritySearchRequest(BaseModel):
    text: str

class SimilaritySearchResponse(BaseModel):
    result: str

class LLMQueryRequest(BaseModel):
    text: str

class LLMQueryResponse(BaseModel):
    response: str