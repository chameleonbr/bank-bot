from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PixTransferRequest(BaseModel):
    pix_key: str
    amount: float
    description: str = ""


class PixScheduleRequest(BaseModel):
    pix_key: str
    amount: float
    schedule_datetime: datetime
    recurrence: str = "none"


class PixKeyOut(BaseModel):
    id: str
    key_type: str
    key_value: str
    status: str

    model_config = {"from_attributes": True}


class PixKeyCreate(BaseModel):
    key_type: str   # cpf | cnpj | email | phone | random
    key_value: str = ""


class PixLimitOut(BaseModel):
    account_id: str
    limit_daytime: float
    limit_nighttime: float


class PixLimitUpdate(BaseModel):
    new_limit_daytime: float
    new_limit_nighttime: float


class PixValidateResponse(BaseModel):
    pix_key: str
    key_type: str
    holder_name: str
    cpf_cnpj: str
    bank: str
    is_valid: bool


class PixReceiptOut(BaseModel):
    transaction_id: str
    date: datetime
    amount: float
    origin_holder: str
    origin_account_id: str
    destination_holder: str
    destination_key: str
    description: str
    status: str


class TransferResponse(BaseModel):
    transaction_id: str
    status: str
    message: str
    timestamp: datetime
