import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.contact import Contact
from app.models.scheduled import ScheduledOperation
from app.schemas.banking import (
    BalanceResponse, StatementResponse, TransactionOut,
    AccountInfoResponse, ContactOut, ContactCreate, ScheduledOperationOut,
)

router = APIRouter(prefix="/banking", tags=["banking"])


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return acc


@router.get("/balance", response_model=BalanceResponse)
def get_balance(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = _get_account(current_user["account_id"], db)
    total = acc.balance_checking + acc.balance_savings + acc.balance_salary
    return BalanceResponse(
        account_id=acc.id,
        holder_name=acc.holder_name,
        balance_checking=acc.balance_checking,
        balance_savings=acc.balance_savings,
        balance_salary=acc.balance_salary,
        balance_total=total,
        updated_at=datetime.now(timezone.utc),
    )


@router.get("/account-info", response_model=AccountInfoResponse)
def get_account_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = _get_account(current_user["account_id"], db)
    return AccountInfoResponse.model_validate(acc)


@router.get("/statement", response_model=StatementResponse)
def get_statement(
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    category: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    acc_id = current_user["account_id"]
    q = db.query(Transaction).filter(Transaction.account_id == acc_id)
    if start_date:
        q = q.filter(Transaction.date >= datetime.fromisoformat(start_date))
    if end_date:
        q = q.filter(Transaction.date <= datetime.fromisoformat(end_date + "T23:59:59"))
    if category:
        q = q.filter(Transaction.category == category)
    transactions = q.order_by(Transaction.date.desc()).limit(limit).all()
    total_debit = sum(t.amount for t in transactions if t.amount < 0)
    total_credit = sum(t.amount for t in transactions if t.amount > 0)
    return StatementResponse(
        account_id=acc_id,
        start_date=start_date or "—",
        end_date=end_date or "—",
        transactions=[TransactionOut.model_validate(t) for t in transactions],
        total_debit=total_debit,
        total_credit=total_credit,
    )


@router.get("/contacts", response_model=list[ContactOut])
def list_contacts(
    search: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Contact).filter(Contact.account_id == current_user["account_id"])
    if search:
        q = q.filter(Contact.name.ilike(f"%{search}%"))
    return [ContactOut.model_validate(c) for c in q.all()]


@router.post("/contacts", response_model=ContactOut, status_code=201)
def add_contact(
    payload: ContactCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = Contact(
        id=f"CON{uuid.uuid4().hex[:6].upper()}",
        account_id=current_user["account_id"],
        **payload.model_dump(),
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return ContactOut.model_validate(contact)


@router.delete("/contacts/{contact_id}", status_code=204)
def remove_contact(
    contact_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.account_id == current_user["account_id"],
    ).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    db.delete(contact)
    db.commit()


@router.get("/scheduled", response_model=list[ScheduledOperationOut])
def get_scheduled(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(ScheduledOperation).filter(
        ScheduledOperation.account_id == current_user["account_id"],
        ScheduledOperation.status == "scheduled",
    )
    if date_from:
        q = q.filter(ScheduledOperation.schedule_datetime >= datetime.fromisoformat(date_from))
    if date_to:
        q = q.filter(ScheduledOperation.schedule_datetime <= datetime.fromisoformat(date_to + "T23:59:59"))
    return [ScheduledOperationOut.model_validate(s) for s in q.order_by(ScheduledOperation.schedule_datetime).all()]


@router.delete("/scheduled/{schedule_id}", status_code=204)
def cancel_scheduled(
    schedule_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    op = db.query(ScheduledOperation).filter(
        ScheduledOperation.id == schedule_id,
        ScheduledOperation.account_id == current_user["account_id"],
    ).first()
    if not op:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    op.status = "cancelled"
    db.commit()
