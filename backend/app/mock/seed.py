"""
Seed script: populates SQLite with all mock data on startup.
Safe to run multiple times (uses merge/upsert pattern).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.mock.data import (
    MOCK_ACCOUNTS, MOCK_USERS, MOCK_PIX_KEYS, MOCK_PIX_LIMITS,
    MOCK_CONTACTS, MOCK_INVESTMENTS, MOCK_LOANS, MOCK_FINANCINGS,
    MOCK_SCHEDULED, MOCK_TICKETS, MOCK_TRANSACTIONS,
)
from app.models.account import Account
from app.models.user import User
from app.models.transaction import Transaction
from app.models.contact import Contact
from app.models.pix_key import PixKey, PixLimit
from app.models.scheduled import ScheduledOperation
from app.models.investment import Investment
from app.models.loan import Loan
from app.models.financing import Financing
from app.models.ticket import Ticket


def _dt(s: str | None) -> datetime | None:
    if s is None:
        return None
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def seed_database() -> None:
    """Create tables and populate with mock data."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        _seed_accounts(db)
        _seed_users(db)
        _seed_pix(db)
        _seed_contacts(db)
        _seed_scheduled(db)
        _seed_investments(db)
        _seed_loans(db)
        _seed_financings(db)
        _seed_tickets(db)
        _seed_transactions(db)
        db.commit()
        print("✅  Mock data seeded successfully.")
    except Exception as exc:
        db.rollback()
        print(f"❌  Seed error: {exc}")
        raise
    finally:
        db.close()


def _seed_accounts(db: Session) -> None:
    for data in MOCK_ACCOUNTS:
        if not db.get(Account, data["id"]):
            db.add(Account(**data))


def _seed_users(db: Session) -> None:
    for data in MOCK_USERS:
        if not db.get(User, data["id"]):
            db.add(User(
                id=data["id"],
                account_id=data["account_id"],
                pin_hash=hash_password(data["pin"]),
            ))


def _seed_pix(db: Session) -> None:
    for data in MOCK_PIX_KEYS:
        if not db.get(PixKey, data["id"]):
            db.add(PixKey(**data))
    for data in MOCK_PIX_LIMITS:
        if not db.get(PixLimit, data["account_id"]):
            db.add(PixLimit(**data))


def _seed_contacts(db: Session) -> None:
    for data in MOCK_CONTACTS:
        if not db.get(Contact, data["id"]):
            db.add(Contact(**data))


def _seed_scheduled(db: Session) -> None:
    for data in MOCK_SCHEDULED:
        if not db.get(ScheduledOperation, data["id"]):
            db.add(ScheduledOperation(
                id=data["id"],
                account_id=data["account_id"],
                type=data["type"],
                amount=data["amount"],
                destination_name=data["destination_name"],
                destination_key=data["destination_key"],
                schedule_datetime=_dt(data["schedule_datetime"]),
                recurrence=data["recurrence"],
                status=data["status"],
            ))


def _seed_investments(db: Session) -> None:
    for data in MOCK_INVESTMENTS:
        if not db.get(Investment, data["id"]):
            db.add(Investment(
                id=data["id"],
                account_id=data["account_id"],
                product_type=data["product_type"],
                product_name=data["product_name"],
                amount_invested=data["amount_invested"],
                current_value=data["current_value"],
                rate=data["rate"],
                start_date=_dt(data["start_date"]),
                maturity_date=_dt(data["maturity_date"]),
                liquidity=data["liquidity"],
                status=data["status"],
            ))


def _seed_loans(db: Session) -> None:
    for data in MOCK_LOANS:
        if not db.get(Loan, data["id"]):
            db.add(Loan(
                id=data["id"],
                account_id=data["account_id"],
                loan_type=data["loan_type"],
                requested_amount=data["requested_amount"],
                outstanding_balance=data["outstanding_balance"],
                installment_amount=data["installment_amount"],
                num_installments=data["num_installments"],
                paid_installments=data["paid_installments"],
                monthly_rate=data["monthly_rate"],
                start_date=_dt(data["start_date"]),
                next_due_date=_dt(data["next_due_date"]),
                status=data["status"],
            ))


def _seed_financings(db: Session) -> None:
    for data in MOCK_FINANCINGS:
        if not db.get(Financing, data["id"]):
            db.add(Financing(
                id=data["id"],
                account_id=data["account_id"],
                modality=data["modality"],
                asset_value=data["asset_value"],
                financed_amount=data["financed_amount"],
                entry_value=data["entry_value"],
                outstanding_balance=data["outstanding_balance"],
                installment_amount=data["installment_amount"],
                num_installments=data["num_installments"],
                paid_installments=data["paid_installments"],
                amortization_system=data["amortization_system"],
                monthly_rate=data["monthly_rate"],
                start_date=_dt(data["start_date"]),
                next_due_date=_dt(data["next_due_date"]),
                status=data["status"],
            ))


def _seed_tickets(db: Session) -> None:
    for data in MOCK_TICKETS:
        if not db.get(Ticket, data["id"]):
            db.add(Ticket(
                id=data["id"],
                account_id=data["account_id"],
                category=data["category"],
                description=data["description"],
                priority=data["priority"],
                status=data["status"],
                created_at=_dt(data["created_at"]),
                updated_at=_dt(data["updated_at"]),
                resolution=data["resolution"],
            ))


def _seed_transactions(db: Session) -> None:
    for data in MOCK_TRANSACTIONS:
        if not db.get(Transaction, data["id"]):
            db.add(Transaction(
                id=data["id"],
                account_id=data["account_id"],
                date=_dt(data["date"]),
                description=data["description"],
                amount=data["amount"],
                category=data["category"],
                type=data["type"],
                counterpart_name=data["counterpart_name"],
                counterpart_key=data["counterpart_key"],
                receipt_id=data["receipt_id"],
                status=data["status"],
            ))
