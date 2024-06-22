from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db, ItemDB
from schemas import ItemCreate, ItemResponse, APIKeyRequest, APIKeyResponse
import secrets

router = APIRouter()

@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    else:
        return {"message": "Item not found"}
    
@router.post("/generate_api_key", response_class=HTMLResponse, include_in_schema=False)
async def generate_api_key(name: str = Form(...), email: str = Form(...)):
    api_key = f"gv_{secrets.token_urlsafe(16)}"
    
    html_response = f"""
    <p>Your API Key: <span class="api-key">{api_key}</span></p>
    <p>Keep this key secure and don't share it publicly!</p>
    """
    return HTMLResponse(content=html_response)