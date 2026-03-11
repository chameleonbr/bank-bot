from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends

from app.core.config import settings

bearer_scheme = HTTPBearer()


def decode_token(token: str) -> dict:
    """Decode and validate JWT, returning the payload."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """FastAPI dependency: returns JWT payload with user_id and account_id."""
    return decode_token(credentials.credentials)


def extract_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """Returns the raw JWT string (forwarded to the backend)."""
    return credentials.credentials
