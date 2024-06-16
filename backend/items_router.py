from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_db, Item

router = APIRouter()

@router.post("/api/items")
def create_item(item: Item, db: Session = Depends(get_db)):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}