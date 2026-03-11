from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate with account_id + PIN and receive a JWT."""
    user = db.query(User).filter(User.account_id == payload.account_id).first()
    if not user or not verify_password(payload.pin, user.pin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account_id or PIN",
        )
    token = create_access_token(
        data={"sub": user.id, "user_id": user.id, "account_id": payload.account_id}
    )
    return TokenResponse(
        access_token=token,
        account_id=payload.account_id,
        holder_name=user.account.holder_name,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Issue a new token given a valid non-expired token."""
    account_id = current_user.get("account_id")
    user = db.query(User).filter(User.account_id == account_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_access_token(
        data={"sub": user.id, "user_id": user.id, "account_id": account_id}
    )
    return TokenResponse(
        access_token=token,
        account_id=account_id,
        holder_name=user.account.holder_name,
    )

