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
from app.models.pix_key import PixKey, PixLimit
from app.models.scheduled import ScheduledOperation
from app.schemas.pix import (
    PixTransferRequest, PixScheduleRequest, PixKeyOut, PixKeyCreate,
    PixLimitOut, PixLimitUpdate, PixValidateResponse, PixReceiptOut, TransferResponse,
)

router = APIRouter(prefix="/pix", tags=["pix"])

# Simulated external PIX directory (for validate_pix_key)
_PIX_DIRECTORY = {
    "joao.silva@email.com":    {"holder_name": "João Silva",      "cpf_cnpj": "111.222.333-44", "bank": "Nubank"},
    "+5511977776666":          {"holder_name": "Maria Fernandes",  "cpf_cnpj": "222.333.444-55", "bank": "Itaú"},
    "+5511999998888":          {"holder_name": "Carlos Eduardo Lima","cpf_cnpj":"234.567.890-12", "bank": "FinBank"},
    "ana.souza@email.com":     {"holder_name": "Ana Paula Souza",  "cpf_cnpj": "123.456.789-01", "bank": "FinBank"},
    "pedro.santos@email.com":  {"holder_name": "Pedro Santos",     "cpf_cnpj": "333.444.555-66", "bank": "Bradesco"},
    "+5511966665555":          {"holder_name": "Luciana Pereira",  "cpf_cnpj": "444.555.666-77", "bank": "Caixa"},
    "financeiro@alpha.com.br": {"holder_name": "Fornecedor Alpha", "cpf_cnpj": "98.765.432/0001-10","bank": "BB"},
    "+5511955554444":          {"holder_name": "Carla Rodrigues",  "cpf_cnpj": "555.666.777-88", "bank": "Inter"},
}


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc


@router.post("/validate", response_model=PixValidateResponse)
def validate_pix_key(pix_key: str, _: dict = Depends(get_current_user)):
    info = _PIX_DIRECTORY.get(pix_key)
    if not info:
        return PixValidateResponse(pix_key=pix_key, key_type="unknown", holder_name="", cpf_cnpj="", bank="", is_valid=False)
    key_type = "email" if "@" in pix_key else "phone" if pix_key.startswith("+") else "cpf"
    return PixValidateResponse(pix_key=pix_key, key_type=key_type, is_valid=True, **info)


@router.post("/transfer", response_model=TransferResponse)
def pix_transfer(
    payload: PixTransferRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    acc = _get_account(current_user["account_id"], db)
    if acc.balance_checking < payload.amount:
        raise HTTPException(status_code=422, detail="Insufficient balance")
    # Simulated 5% failure rate
    if random.random() < 0.05:
        raise HTTPException(status_code=503, detail="PIX transaction failure. Try again.")
    acc.balance_checking -= payload.amount
    recipient = _PIX_DIRECTORY.get(payload.pix_key, {})
    txn_id = f"TRX{uuid.uuid4().hex[:8].upper()}"
    db.add(Transaction(
        id=txn_id,
        account_id=acc.id,
        description=f"PIX sent - {recipient.get('holder_name', payload.pix_key)}",
        amount=-payload.amount,
        category="transfer",
        type="pix",
        counterpart_name=recipient.get("holder_name", ""),
        counterpart_key=payload.pix_key,
        receipt_id=f"RCP{uuid.uuid4().hex[:6].upper()}",
        status="completed",
    ))
    db.commit()
    return TransferResponse(transaction_id=txn_id, status="completed", message="PIX sent successfully!", timestamp=datetime.now(timezone.utc))


@router.post("/schedule", status_code=201)
def pix_schedule(
    payload: PixScheduleRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipient = _PIX_DIRECTORY.get(payload.pix_key, {})
    op = ScheduledOperation(
        id=f"SCH{uuid.uuid4().hex[:6].upper()}",
        account_id=current_user["account_id"],
        type="pix",
        amount=payload.amount,
        destination_name=recipient.get("holder_name", ""),
        destination_key=payload.pix_key,
        schedule_datetime=payload.schedule_datetime,
        recurrence=payload.recurrence,
    )
    db.add(op)
    db.commit()
    return {"schedule_id": op.id, "status": "scheduled", "message": "PIX scheduled successfully!"}


@router.get("/keys", response_model=list[PixKeyOut])
def get_pix_keys(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    keys = db.query(PixKey).filter(
        PixKey.account_id == current_user["account_id"],
        PixKey.status == "active"
    ).all()
    return [PixKeyOut.model_validate(k) for k in keys]


@router.post("/keys", response_model=PixKeyOut, status_code=201)
def register_pix_key(
    payload: PixKeyCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    key_value = payload.key_value or str(uuid.uuid4())  # random key
    key = PixKey(
        id=f"PIX{uuid.uuid4().hex[:6].upper()}",
        account_id=current_user["account_id"],
        key_type=payload.key_type,
        key_value=key_value,
        status="active",
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return PixKeyOut.model_validate(key)


@router.delete("/keys/{pix_key_id}", status_code=204)
def delete_pix_key(
    pix_key_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    key = db.query(PixKey).filter(
        PixKey.id == pix_key_id,
        PixKey.account_id == current_user["account_id"],
    ).first()
    if not key:
        raise HTTPException(status_code=404, detail="PIX key not found")
    key.status = "deleted"
    db.commit()


@router.get("/limits", response_model=PixLimitOut)
def get_pix_limits(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    limits = db.get(PixLimit, current_user["account_id"])
    if not limits:
        raise HTTPException(status_code=404, detail="Limits not configured")
    return PixLimitOut(account_id=limits.account_id, limit_daytime=limits.limit_daytime, limit_nighttime=limits.limit_nighttime)


@router.put("/limits", response_model=PixLimitOut)
def update_pix_limit(
    payload: PixLimitUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Updates the PIX limits for the user."""
    limits = db.get(PixLimit, current_user["account_id"])
    if not limits:
        raise HTTPException(status_code=404, detail="Limits not found")
    limits.limit_daytime = payload.new_limit_daytime
    limits.limit_nighttime = payload.new_limit_nighttime
    db.commit()
    return PixLimitOut(account_id=limits.account_id, limit_daytime=limits.limit_daytime, limit_nighttime=limits.limit_nighttime)


@router.get("/receipt/{transaction_id}", response_model=PixReceiptOut)
def get_pix_receipt(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    txn = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.account_id == current_user["account_id"],
        Transaction.type == "pix",
    ).first()
    if not txn:
        raise HTTPException(status_code=404, detail="Receipt not found")
    acc = db.get(Account, current_user["account_id"])
    return PixReceiptOut(
        transaction_id=txn.id,
        date=txn.date,
        amount=abs(txn.amount),
        origin_holder=acc.holder_name,
        origin_account_id=acc.id,
        destination_holder=txn.counterpart_name,
        destination_key=txn.counterpart_key,
        description=txn.description,
        status=txn.status,
    )
