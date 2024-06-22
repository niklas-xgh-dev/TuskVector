from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(ItemCreate):
    id: int

    class Config:
        orm_mode = True

class APIKeyRequest(BaseModel):
    name: str
    email: str

class APIKeyResponse(BaseModel):
    api_key: str