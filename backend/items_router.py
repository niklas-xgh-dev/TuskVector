from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db, ItemDB, get_api_key
from .schemas import ItemCreate, ItemResponse
from .rate_limiter import rate_limit

router = APIRouter()

@router.get("/items/{item_id}", response_model=ItemResponse, include_in_schema=False)
@rate_limit(limit = 10, period = 3600)
def get_item(item_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=ItemResponse, include_in_schema=False)
@rate_limit(limit = 10, period = 3600)
def create_item(item: ItemCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", include_in_schema=False)
@rate_limit(limit = 10, period = 3600)
def delete_item(item_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}