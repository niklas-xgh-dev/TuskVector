from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, ItemDB, ApiKeyDB, get_api_key
from schemas import ItemCreate, ItemResponse
import secrets
from datetime import datetime

router = APIRouter()

def get_client_ip(request: Request):
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    return cf_connecting_ip or request.client.host

@router.get("/items/{item_id}", response_model=ItemResponse, include_in_schema=False)
def get_item(item_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=ItemResponse, include_in_schema=False)
def create_item(item: ItemCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", include_in_schema=False)
def delete_item(item_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
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
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)

    existing_key = db.query(ApiKeyDB).filter(
        (ApiKeyDB.email == email) | (ApiKeyDB.source_ip == client_ip)
    ).first()

    if existing_key:
        error_message = "Your system already received an API key. In case you lost it, please contact the administrator."
        return HTMLResponse(content=f'<p class="error"><i>{error_message}</i></p>', status_code=200)

    api_key = f"gv_{secrets.token_urlsafe(16)}"
    
    new_api_key = ApiKeyDB(
        key=api_key,
        email=email,
        source_ip=client_ip,
        created_at=datetime.utcnow(),
        last_used_at=datetime.utcnow()
    )

    try:
        db.add(new_api_key)
        db.commit()
    except IntegrityError:
        db.rollback()
        error_message = "Unable to generate API key. Please try again."
        return HTMLResponse(content=f'<p class="error"><i>{error_message}</i></p>', status_code=200)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - API key generated for {email} from IP: {client_ip}")
    
    success_message = f"""
    <p class="success"><i>Your API Key: <span class="api-key">{api_key}</span></i></p>
    <p><i>You thought we would send it via email? That would not be XGH.</i></p>
    <p><i>Save this key securely NOW and don't share it publicly.</i></p>
    """
    return HTMLResponse(content=success_message, status_code=200)