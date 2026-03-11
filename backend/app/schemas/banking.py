from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class BalanceResponse(BaseModel):
    account_id: str
    holder_name: str
    balance_checking: float
    balance_savings: float
    balance_salary: float
    balance_total: float
    updated_at: datetime


class TransactionOut(BaseModel):
    id: str
    date: datetime
    description: str
    amount: float
    category: str
    type: str
    counterpart_name: str
    status: str

    model_config = {"from_attributes": True}


class StatementResponse(BaseModel):
    account_id: str
    start_date: str
    end_date: str
    transactions: List[TransactionOut]
    total_debit: float
    total_credit: float


class AccountInfoResponse(BaseModel):
    account_id: str
    holder_name: str
    cpf_cnpj: str
    account_type: str
    investor_profile: str
    credit_score: float
    manager_name: str
    manager_phone: str
    manager_email: str
    branch_name: str
    branch_address: str
    branch_phone: str

    model_config = {"from_attributes": True}


class ContactOut(BaseModel):
    id: str
    name: str
    cpf_cnpj: str
    bank: str
    agency: str
    account_number: str
    pix_key: str
    alias: str

    model_config = {"from_attributes": True}


class ContactCreate(BaseModel):
    name: str
    cpf_cnpj: str
    bank: str = ""
    bank_code: str = ""
    agency: str = ""
    account_number: str = ""
    pix_key: str = ""
    alias: str = ""


class ScheduledOperationOut(BaseModel):
    id: str
    type: str
    amount: float
    destination_name: str
    destination_key: str
    schedule_datetime: datetime
    recurrence: str
    status: str

    model_config = {"from_attributes": True}
