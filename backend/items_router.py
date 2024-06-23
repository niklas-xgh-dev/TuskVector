from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, ItemDB, ApiKeyDB
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
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # Get the true client IP
    client_ip = get_client_ip(request)

    # Check if email or IP already has an API key
    existing_key = db.query(ApiKeyDB).filter(
        (ApiKeyDB.email == email) | (ApiKeyDB.source_ip == client_ip)
    ).first()

    if existing_key:
        error_message = "Your system already received an API key. In case you lost it, please contact the administrator."
        return HTMLResponse(content=f'<p class="error"><i>{error_message}</i></p>', status_code=200)

    # Generate the API key
    api_key = f"gv_{secrets.token_urlsafe(16)}"
    
    # Create new ApiKeyDB instance
    new_api_key = ApiKeyDB(
        key=api_key,
        email=email,
        source_ip=client_ip,
        created_at=datetime.utcnow(),
        last_used_at=datetime.utcnow()
    )

    try:
        # Add to database and commit
        db.add(new_api_key)
        db.commit()
    except IntegrityError:
        db.rollback()
        error_message = "Unable to generate API key. Please try again."
        return HTMLResponse(content=f'<p class="error"><i>{error_message}</i></p>', status_code=200)

    # Log the API key generation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - API key generated for {email} from IP: {client_ip}")
    
    success_message = f"""
    <p class="success"><i>Your API Key: <span class="api-key">{api_key}</span></i></p>
    <p><i>You thought we would send it via email? That would not be XGH.</i></p>
    <p><i>Save this key securely NOW and don't share it publicly.</i></p>
    """
    return HTMLResponse(content=success_message, status_code=200)