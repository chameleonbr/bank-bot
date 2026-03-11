from pydantic import BaseModel


class LoginRequest(BaseModel):
    account_id: str
    pin: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    account_id: str
    holder_name: str
