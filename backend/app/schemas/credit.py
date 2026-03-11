from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CreditLimitOut(BaseModel):
    account_id: str
    total_limit: float
    used_limit: float
    available_limit: float


class SimulateLoanRequest(BaseModel):
    amount: float
    num_installments: int
    loan_type: str = "pessoal"  # pessoal | consignado | empresarial


class SimulateLoanResponse(BaseModel):
    loan_type: str
    amount: float
    num_installments: int
    installment_amount: float
    monthly_rate_percent: float
    annual_rate_percent: float
    total_amount: float
    cet_monthly: float
    cet_annual: float


class RequestLoanRequest(BaseModel):
    amount: float
    num_installments: int
    loan_type: str = "pessoal"
    purpose: str = ""


class LoanOut(BaseModel):
    id: str
    loan_type: str
    requested_amount: float
    outstanding_balance: float
    installment_amount: float
    num_installments: int
    paid_installments: int
    monthly_rate: float
    next_due_date: datetime
    status: str

    model_config = {"from_attributes": True}


class AnticipateRequest(BaseModel):
    loan_id: str
    num_installments_to_anticipate: int


class AnticipateResponse(BaseModel):
    loan_id: str
    installments_to_anticipate: int
    original_total: float
    discount: float
    amount_to_pay: float
    new_outstanding_balance: float


class CreditScoreOut(BaseModel):
    account_id: str
    score: int
    classification: str   # Baixo | Regular | Bom | Ótimo | Excelente
    updated_at: str


# --- Financing ---

class SimulateFinancingRequest(BaseModel):
    amount: float
    entry_value: float
    period_months: int
    modality: str       # imovel | veiculo | rural
    system: str = "SAC"  # SAC | PRICE | MISTO


class SimulateFinancingResponse(BaseModel):
    modality: str
    system: str
    asset_value: float
    entry_value: float
    financed_amount: float
    period_months: int
    first_installment: float
    last_installment: float
    total_amount: float
    monthly_rate_percent: float


class FinancingOut(BaseModel):
    id: str
    modality: str
    asset_value: float
    financed_amount: float
    outstanding_balance: float
    installment_amount: float
    num_installments: int
    paid_installments: int
    amortization_system: str
    next_due_date: datetime
    status: str

    model_config = {"from_attributes": True}


class NextInstallmentOut(BaseModel):
    financing_id: str
    due_date: datetime
    amount: float
    installment_number: int
    total_installments: int
