from datetime import datetime
from typing import List
from pydantic import BaseModel


class TedTransferRequest(BaseModel):
    bank_code: str
    agency: str
    account_number: str
    cpf_cnpj: str
    amount: float
    description: str = ""


class TedScheduleRequest(BaseModel):
    bank_code: str
    agency: str
    account_number: str
    cpf_cnpj: str
    amount: float
    schedule_date: str  # YYYY-MM-DD


class TedValidateRequest(BaseModel):
    bank_code: str
    agency: str
    account_number: str
    cpf_cnpj: str


class TedValidateResponse(BaseModel):
    is_valid: bool
    holder_name: str
    bank_name: str


class TedLimitOut(BaseModel):
    account_id: str
    daily_limit: float
    used_today: float
    available: float


class BankOut(BaseModel):
    code: str
    ispb: str
    name: str
    short_name: str


class TransferResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    timestamp: datetime
