from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db, ItemDB
from schemas import ItemCreate, ItemResponse, APIKeyRequest, APIKeyResponse
import secrets
from datetime import datetime

router = APIRouter()

def get_client_ip(request: Request):
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    return cf_connecting_ip or request.client.host

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
async def generate_api_key(
    request: Request,
    name: str = Form(...), 
    email: str = Form(...)
):
    # Get the true client IP
    client_ip = get_client_ip(request)

    # Generate the API key
    api_key = f"gv_{secrets.token_urlsafe(16)}"
    
    # Log the API key generation with the true client IP
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - API key generated for {email} from IP: {client_ip}")
    
    html_response = f"""
    <p>Your API Key: <span class="api-key">{api_key}</span></p>
    <p>Keep this key secure and don't share it publicly!</p>
    """
    return HTMLResponse(content=html_response)