from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.db import get_db
from backend.app.models.models import User
from backend.app.services.gmail_auth import (
    get_gmail_auth_url,
    exchange_code_for_token,
)

router = APIRouter(tags=["Auth"])


# -----------------------------------
# Health / Test endpoint
# -----------------------------------
@router.post("/login")
def login():
    return {"message": "Auth service working"}


# -----------------------------------
# Gmail OAuth – Step 1
# -----------------------------------
@router.get("/gmail/login/{user_id}")
def gmail_login(user_id: int, db: Session = Depends(get_db)):
    """
    Returns Google OAuth URL for Gmail access
    """

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    auth_url, state = get_gmail_auth_url(user_id)

    return {
        "auth_url": auth_url,
        "state": state,
    }


# -----------------------------------
# Gmail OAuth – Step 2 (Callback)
# -----------------------------------
@router.get("/gmail/callback")
def gmail_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Handles Google OAuth callback and stores tokens
    """

    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state")

    # Extract user_id from state
    try:
        user_id = int(state.split("_")[1])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    token_data = exchange_code_for_token(code)

    # Store token in DB (raw SQL to keep simple & safe)
    db.execute(
        """
        INSERT INTO gmail_tokens (user_id, access_token, refresh_token, token_expiry, created_at)
        VALUES (:user_id, :access_token, :refresh_token, :expiry, :created_at)
        ON CONFLICT (user_id)
        DO UPDATE SET
            access_token = EXCLUDED.access_token,
            refresh_token = EXCLUDED.refresh_token,
            token_expiry = EXCLUDED.token_expiry,
            created_at = EXCLUDED.created_at
        """,
        {
            "user_id": user_id,
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expiry": token_data["expiry"],
            "created_at": datetime.utcnow(),
        },
    )

    db.commit()

    return {
        "message": "Gmail connected successfully",
        "user_id": user_id,
    }
