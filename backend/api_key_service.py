import os
import secrets
import logging
import smtplib

from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db, ApiKeyDB

router = APIRouter()

# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def get_client_ip(request: Request):
    cf = request.headers.get("CF-Connecting-IP")
    return cf or request.client.host

@router.post("/generate_api_key", response_class=HTMLResponse)
async def generate_api_key(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    client_ip = get_client_ip(request)
    logging.info(f"Received API key request from {email} @ {client_ip}")

    # check for existing
    existing = db.query(ApiKeyDB).filter(
        (ApiKeyDB.email == email) | (ApiKeyDB.source_ip == client_ip)
    ).first()
    if existing:
        logging.warning(f"API key already exists for {email} or IP {client_ip}")
        return HTMLResponse(
            content='<p class="error"><i>Your system already received an API key. '
                    'In case you lost it, please contact the administrator.</i></p>',
            status_code=200
        )

    # generate & save
    api_key = f"gv_{secrets.token_urlsafe(16)}"
    new_key = ApiKeyDB(
        key=api_key,
        email=email,
        source_ip=client_ip,
        created_at=datetime.utcnow(),
        last_used_at=datetime.utcnow(),
    )
    try:
        db.add(new_key)
        db.commit()
        logging.info(f"Stored new API key for {email}")
    except IntegrityError as e:
        db.rollback()
        logging.error(f"DB IntegrityError: {e}")
        return HTMLResponse(
            content='<p class="error"><i>Unable to generate API key. Please try again.</i></p>',
            status_code=200
        )

    # send email
    success, err = send_api_key_email(email, api_key)
    if success:
        logging.info(f"Email sent successfully to {email}")
    else:
        logging.error(f"Failed to send API key email to {email}: {err}")

    return HTMLResponse(
        content="Thanks for testing TuskVector, the API key is on the way to your inbox!",
        status_code=200
    )


def send_api_key_email(recipient: str, api_key: str):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    logging.debug(f"SENDER_EMAIL={sender_email!r}, password set? {bool(sender_password)}")

    if not sender_email or not sender_password:
        err = "Sender email or password not set in environment variables"
        logging.error(err)
        return False, err

    # build message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your TuskVector API Key"
    message["From"] = sender_email
    message["To"] = recipient

    text = f"Your TuskVector API Key is: {api_key}\n\nPlease keep this key secure."
    html = f"""
    <html>
      <body>
        <h2>Your TuskVector 🐘 API Key</h2>
        <p><strong>{api_key}</strong></p>
        <p>Please keep this key secure and do not share it publicly.</p>
      </body>
    </html>
    """

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    try:
        logging.debug("Connecting to SMTP server smtp.gmail.com:465")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            logging.debug(f"Logging in as {sender_email}")
            server.login(sender_email, sender_password)
            logging.debug(f"Sending email to {recipient}")
            server.sendmail(sender_email, recipient, message.as_string())
        return True, None
    except Exception as e:
        logging.exception("Exception while sending email")
        return False, str(e)
