import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import Account
from app.models.loan import Loan
from app.models.financing import Financing
from app.schemas.credit import (
    CreditLimitOut, SimulateLoanRequest, SimulateLoanResponse,
    RequestLoanRequest, LoanOut, AnticipateRequest, AnticipateResponse,
    CreditScoreOut, SimulateFinancingRequest, SimulateFinancingResponse,
    FinancingOut, NextInstallmentOut,
)

router = APIRouter(prefix="/credit", tags=["credit"])

_SCORE_CLASSIFICATION = [
    (620, "Low"), (700, "Regular"), (750, "Good"), (820, "Great"), (float("inf"), "Excellent")
]

LOAN_RATES = {"pessoal": 0.0199, "consignado": 0.0114, "empresarial": 0.0149}
FINANCING_RATES = {"imovel": 0.0075, "veiculo": 0.0099, "rural": 0.0089}


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc


def _pmt(principal: float, rate: float, n: int) -> float:
    """Price table installment."""
    if rate == 0:
        return principal / n
    return principal * (rate * (1 + rate) ** n) / ((1 + rate) ** n - 1)


@router.get("/limit", response_model=CreditLimitOut)
def get_credit_limit(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns the user's total, used, and available credit limit."""
    acc = _get_account(current_user["account_id"], db)
    total = acc.credit_score * 50  # simple formula
    used = sum(l.outstanding_balance for l in acc.loans if l.status == "active")
    return CreditLimitOut(account_id=acc.id, total_limit=round(total), used_limit=round(used, 2), available_limit=round(max(0, total - used), 2))


@router.post("/simulate-loan", response_model=SimulateLoanResponse)
def simulate_loan(payload: SimulateLoanRequest, current_user: dict = Depends(get_current_user)):
    """Simulates a loan with installments and specific rates."""
    rate = LOAN_RATES.get(payload.loan_type, 0.0199)
    installment = _pmt(payload.amount, rate, payload.num_installments)
    total = installment * payload.num_installments
    cet = rate * 1.02  # simplified CET
    return SimulateLoanResponse(
        loan_type=payload.loan_type, amount=payload.amount,
        num_installments=payload.num_installments,
        installment_amount=round(installment, 2),
        monthly_rate_percent=round(rate * 100, 2),
        annual_rate_percent=round(((1 + rate) ** 12 - 1) * 100, 2),
        total_amount=round(total, 2), cet_monthly=round(cet * 100, 2),
        cet_annual=round(((1 + cet) ** 12 - 1) * 100, 2),
    )


@router.post("/request-loan", status_code=201)
def request_loan(
    payload: RequestLoanRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submits a loan request for analysis."""
    acc = _get_account(current_user["account_id"], db)
    rate = LOAN_RATES.get(payload.loan_type, 0.0199)
    installment = _pmt(payload.amount, rate, payload.num_installments)
    loan = Loan(
        id=f"LOA{uuid.uuid4().hex[:6].upper()}",
        account_id=acc.id, loan_type=payload.loan_type,
        requested_amount=payload.amount, outstanding_balance=payload.amount,
        installment_amount=round(installment, 2),
        num_installments=payload.num_installments, paid_installments=0,
        monthly_rate=rate, start_date=datetime.now(timezone.utc),
        next_due_date=datetime.now(timezone.utc), status="analysis",
    )
    db.add(loan)
    db.commit()
    return {"loan_id": loan.id, "status": "analysis", "message": "Request sent. You will receive a response within 1 business day."}


@router.get("/loans", response_model=list[LoanOut])
def list_active_loans(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists all active loans for the user."""
    loans = db.query(Loan).filter(
        Loan.account_id == current_user["account_id"], Loan.status == "active"
    ).all()
    return [LoanOut.model_validate(l) for l in loans]


@router.get("/loan-status/{loan_id}")
def get_loan_status(loan_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns the status of a specific loan request."""
    loan = db.query(Loan).filter(Loan.id == loan_id, Loan.account_id == current_user["account_id"]).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"loan_id": loan.id, "status": loan.status, "type": loan.loan_type, "amount": loan.requested_amount}


@router.get("/loans/{loan_id}/statement")
def get_loan_statement(loan_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns a detailed statement of installments and balance for a loan."""
    loan = db.query(Loan).filter(Loan.id == loan_id, Loan.account_id == current_user["account_id"]).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {
        "loan_id": loan.id, "type": loan.loan_type,
        "requested_amount": loan.requested_amount, "outstanding_balance": loan.outstanding_balance,
        "paid_installments": loan.paid_installments, "num_installments": loan.num_installments,
        "installment_amount": loan.installment_amount, "monthly_rate_pct": round(loan.monthly_rate * 100, 2),
    }


@router.post("/anticipate", response_model=AnticipateResponse)
def anticipate_installments(payload: AnticipateRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Simulates or calculates the discount for anticipating loan installments."""
    loan = db.query(Loan).filter(Loan.id == payload.loan_id, Loan.account_id == current_user["account_id"], Loan.status == "active").first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    original = round(loan.installment_amount * payload.num_installments_to_anticipate, 2)
    discount_rate = 0.005 * payload.num_installments_to_anticipate
    discount = round(original * min(discount_rate, 0.15), 2)
    to_pay = round(original - discount, 2)
    new_balance = round(max(0, loan.outstanding_balance - to_pay), 2)
    return AnticipateResponse(
        loan_id=loan.id, installments_to_anticipate=payload.num_installments_to_anticipate,
        original_total=original, discount=discount, amount_to_pay=to_pay, new_outstanding_balance=new_balance,
    )


@router.get("/score", response_model=CreditScoreOut)
def get_credit_score(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns the user's credit score and classification."""
    acc = _get_account(current_user["account_id"], db)
    score = int(acc.credit_score)
    classification = next(c for threshold, c in _SCORE_CLASSIFICATION if score <= threshold)
    return CreditScoreOut(account_id=acc.id, score=score, classification=classification, updated_at=datetime.now(timezone.utc).date().isoformat())


# ── Financing routes (grouped under /credit for simplicity) ──────────────────

@router.post("/simulate-financing", response_model=SimulateFinancingResponse)
def simulate_financing(payload: SimulateFinancingRequest, _: dict = Depends(get_current_user)):
    """Simulates asset financing (Price or SAC systems)."""
    financed = payload.amount - payload.entry_value
    rate = FINANCING_RATES.get(payload.modality, 0.0085)
    first = _pmt(financed, rate, payload.period_months)
    last = financed / payload.period_months if payload.system == "SAC" else first
    total = first * payload.period_months
    return SimulateFinancingResponse(
        modality=payload.modality, system=payload.system,
        asset_value=payload.amount, entry_value=payload.entry_value,
        financed_amount=round(financed, 2), period_months=payload.period_months,
        first_installment=round(first, 2), last_installment=round(last, 2),
        total_amount=round(total, 2), monthly_rate_percent=round(rate * 100, 2),
    )


@router.get("/financings", response_model=list[FinancingOut])
def list_active_financings(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists all active financing contracts for the user."""
    fins = db.query(Financing).filter(Financing.account_id == current_user["account_id"], Financing.status == "active").all()
    return [FinancingOut.model_validate(f) for f in fins]


@router.get("/financings/{financing_id}/next-installment", response_model=NextInstallmentOut)
def get_next_installment(financing_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns details of the next financing installment due."""
    fin = db.query(Financing).filter(Financing.id == financing_id, Financing.account_id == current_user["account_id"]).first()
    if not fin:
        raise HTTPException(status_code=404, detail="Financing not found")
    return NextInstallmentOut(
        financing_id=fin.id, due_date=fin.next_due_date,
        amount=fin.installment_amount,
        installment_number=fin.paid_installments + 1,
        total_installments=fin.num_installments,
    )


@router.get("/financings/{financing_id}/statement")
def get_financing_statement(financing_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns a statement for a specific financing contract."""
    fin = db.query(Financing).filter(Financing.id == financing_id, Financing.account_id == current_user["account_id"]).first()
    if not fin:
        raise HTTPException(status_code=404, detail="Financing not found")
    return {
        "financing_id": fin.id, "modality": fin.modality, "asset_value": fin.asset_value,
        "financed_amount": fin.financed_amount, "outstanding_balance": fin.outstanding_balance,
        "paid_installments": fin.paid_installments, "num_installments": fin.num_installments,
        "system": fin.amortization_system, "monthly_rate_pct": round(fin.monthly_rate * 100, 3),
    }


@router.post("/financings/request", status_code=201)
def request_financing(
    payload: SimulateFinancingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submits a financing request."""
    acc = _get_account(current_user["account_id"], db)
    rate = FINANCING_RATES.get(payload.modality, 0.0085)
    financed = payload.amount - payload.entry_value
    installment = _pmt(financed, rate, payload.period_months)
    fin = Financing(
        id=f"FIN{uuid.uuid4().hex[:6].upper()}",
        account_id=acc.id, modality=payload.modality,
        asset_value=payload.amount, financed_amount=round(financed, 2),
        entry_value=payload.entry_value, outstanding_balance=round(financed, 2),
        installment_amount=round(installment, 2),
        num_installments=payload.period_months, paid_installments=0,
        amortization_system=payload.system, monthly_rate=rate,
        start_date=datetime.now(timezone.utc), next_due_date=datetime.now(timezone.utc),
        status="analysis",
    )
    db.add(fin)
    db.commit()
    return {"financing_id": fin.id, "status": "analysis", "message": "Financing request registered. You will receive a response within 3 business days."}


@router.post("/financings/{financing_id}/portability")
def request_portability(financing_id: str, target_bank_code: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    fin = db.query(Financing).filter(Financing.id == financing_id, Financing.account_id == current_user["account_id"]).first()
    if not fin:
        raise HTTPException(status_code=404, detail="Financing not found")
    return {"financing_id": fin.id, "target_bank_code": target_bank_code, "status": "requested", "message": "Portability request registered. Documentation will be requested via email within 2 business days."}
