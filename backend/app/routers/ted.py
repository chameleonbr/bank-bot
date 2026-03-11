import uuid
import random
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.scheduled import ScheduledOperation
from app.mock.data import MOCK_BANKS
from app.schemas.ted import (
    TedTransferRequest, TedScheduleRequest, TedValidateRequest,
    TedValidateResponse, TedLimitOut, BankOut, TransferResponse,
)

router = APIRouter(prefix="/ted", tags=["ted"])

_TED_OPEN_HOUR = 6
_TED_CLOSE_HOUR = 17

# Simulated recipient directory for TED validation
_TED_DIRECTORY = {
    ("260", "0001", "1234567-8"): {"holder_name": "João Silva",      "bank_name": "Nubank"},
    ("341", "1234", "9876543-2"): {"holder_name": "Maria Fernandes",  "bank_name": "Itaú"},
    ("237", "5678", "5432109-8"): {"holder_name": "Pedro Santos",     "bank_name": "Bradesco"},
}


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc


@router.post("/validate", response_model=TedValidateResponse)
def validate_ted_dest(payload: TedValidateRequest, _: dict = Depends(get_current_user)):
    key = (payload.bank_code, payload.agency, payload.account_number)
    info = _TED_DIRECTORY.get(key)
    if not info:
        return TedValidateResponse(is_valid=False, holder_name="", bank_name="")
    return TedValidateResponse(is_valid=True, **info)


@router.post("/transfer", response_model=TransferResponse)
def ted_transfer(
    payload: TedTransferRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    if not (_TED_OPEN_HOUR <= now.hour < _TED_CLOSE_HOUR) or now.weekday() >= 5:
        raise HTTPException(
            status_code=422,
            detail=f"TED is only available on business days between {_TED_OPEN_HOUR}h and {_TED_CLOSE_HOUR}h.",
        )
    acc = _get_account(current_user["account_id"], db)
    if acc.balance_checking < payload.amount:
        raise HTTPException(status_code=422, detail="Insufficient balance")
    acc.balance_checking -= payload.amount
    bank = next((b for b in MOCK_BANKS if b["code"] == payload.bank_code), {"short_name": payload.bank_code})
    txn_id = f"TRX{uuid.uuid4().hex[:8].upper()}"
    db.add(Transaction(
        id=txn_id, account_id=acc.id,
        description=f"TED sent - {bank['short_name']} Br.{payload.agency}",
        amount=-payload.amount, category="transfer", type="ted",
        counterpart_name="", counterpart_key="",
        receipt_id=f"RCP{uuid.uuid4().hex[:6].upper()}", status="completed",
    ))
    db.commit()
    return TransferResponse(transaction_id=txn_id, status="completed", message="TED sent successfully!", timestamp=now)


@router.post("/schedule", status_code=201)
def ted_schedule(
    payload: TedScheduleRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bank = next((b for b in MOCK_BANKS if b["code"] == payload.bank_code), {"short_name": payload.bank_code})
    op = ScheduledOperation(
        id=f"SCH{uuid.uuid4().hex[:6].upper()}",
        account_id=current_user["account_id"],
        type="ted", amount=payload.amount,
        destination_name=bank["short_name"],
        destination_key=f"Ag.{payload.agency} Cc.{payload.account_number}",
        schedule_datetime=datetime.fromisoformat(payload.schedule_date + "T10:00:00"),
        recurrence="none",
    )
    db.add(op)
    db.commit()
    return {"schedule_id": op.id, "status": "scheduled", "message": "TED scheduled successfully!"}


@router.get("/receipt/{transaction_id}")
def get_ted_receipt(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    txn = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.account_id == current_user["account_id"],
        Transaction.type == "ted",
    ).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Receipt not found")
    acc = db.get(Account, current_user["account_id"])
    return {
        "transaction_id": txn.id, "date": txn.date, "amount": abs(txn.amount),
        "origin_holder": acc.holder_name, "description": txn.description, "status": txn.status,
    }


@router.get("/limits", response_model=TedLimitOut)
def get_ted_limits(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = _get_account(current_user["account_id"], db)
    daily_limit = 50000.0 if acc.account_type == "PJ" else 10000.0
    used = sum(
        abs(t.amount) for t in db.query(Transaction).filter(
            Transaction.account_id == acc.id, Transaction.type == "ted",
            Transaction.date >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0),
        ).all()
    )
    return TedLimitOut(account_id=acc.id, daily_limit=daily_limit, used_today=used, available=max(0, daily_limit - used))


@router.get("/banks", response_model=list[BankOut])
def list_banks(
    search: Optional[str] = Query(None),
    _: dict = Depends(get_current_user),
):
    banks = MOCK_BANKS
    if search:
        sl = search.lower()
        banks = [b for b in banks if sl in b["name"].lower() or sl in b["short_name"].lower() or sl in b["code"]]
    return [BankOut(**b) for b in banks]
