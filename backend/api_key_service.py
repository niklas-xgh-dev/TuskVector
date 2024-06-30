from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import get_db, ApiKeyDB
import secrets
from datetime import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()

def get_client_ip(request: Request):
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    return cf_connecting_ip or request.client.host
    
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
    
    send_api_key_email(email, api_key)

    success_message = "Thanks for testing TuskVector, the API key is on the way to your inbox!"
    return HTMLResponse(content=success_message, status_code=200)

def send_api_key_email(recipient: str, api_key: str):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        return False, "Sender email or password not set in environment variables"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your TuskVector API Key"
    message["From"] = sender_email
    message["To"] = recipient

    text = f"""
    Your TuskVector API Key is: {api_key}

    Please keep this key secure and do not share it publicly.
    """

    html = f"""
    <html>
      <body>
        <h2>Your TuskVector 🐘 API Key</h2>
        <p><strong>{api_key}</strong></p>
        <p></p>
        <p>Please keep this key secure and do not share it publicly.</p>
        <p>Your request limit was set to 10 requests per hour per endpoint</p>
        <p>If you have any questions or concerns, please contact our support team.</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
        return True, None
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"