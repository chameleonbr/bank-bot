import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import Account
from app.models.ticket import Ticket
from app.mock.data import FAQ_DATA
from app.schemas.support import (
    OpenTicketRequest, TicketOut, ScheduleManagerCallRequest,
    SendManagerMessageRequest, ManagerCallResponse, EscalateRequest,
    EscalateResponse, FAQResponse, BranchInfoOut,
)

router = APIRouter(prefix="/support", tags=["support"])


def _get_account(account_id: str, db: Session) -> Account:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc


@router.post("/tickets", response_model=TicketOut, status_code=201)
def open_ticket(
    payload: OpenTicketRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Opens a new support ticket."""
    ticket = Ticket(
        id=f"TIC{uuid.uuid4().hex[:6].upper()}",
        account_id=current_user["account_id"],
        category=payload.category,
        description=payload.description,
        priority=payload.priority,
        status="open",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return TicketOut.model_validate(ticket)


@router.get("/tickets", response_model=list[TicketOut])
def list_open_tickets(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lists all open or in-progress tickets for the user."""
    tickets = db.query(Ticket).filter(
        Ticket.account_id == current_user["account_id"],
        Ticket.status.in_(["open", "in_progress"]),
    ).all()
    return [TicketOut.model_validate(t) for t in tickets]


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket_status(ticket_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns the status and details of a specific ticket."""
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id, Ticket.account_id == current_user["account_id"]
    ).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketOut.model_validate(ticket)


@router.post("/manager/schedule", response_model=ManagerCallResponse)
def schedule_manager_call(
    payload: ScheduleManagerCallRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Schedules a call with the account manager."""
    acc = _get_account(current_user["account_id"], db)
    return ManagerCallResponse(
        confirmation_id=f"CAL{uuid.uuid4().hex[:6].upper()}",
        manager_name=acc.manager_name,
        scheduled_date=payload.preferred_date,
        scheduled_time=payload.preferred_time,
        subject=payload.subject,
        message=f"Call scheduled with {acc.manager_name} on {payload.preferred_date} at {payload.preferred_time}. A reminder will be sent by email.",
    )


@router.post("/manager/message")
def send_message_to_manager(
    payload: SendManagerMessageRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sends a message to the account manager."""
    acc = _get_account(current_user["account_id"], db)
    return {
        "message_id": f"MSG{uuid.uuid4().hex[:6].upper()}",
        "to": acc.manager_name,
        "category": payload.category,
        "status": "sent",
        "message": "Message sent to your manager. Expected response within 1 business day.",
    }


@router.get("/manager")
def get_manager_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns contact info for the account manager."""
    acc = _get_account(current_user["account_id"], db)
    return {
        "account_id": acc.id,
        "manager_name": acc.manager_name,
        "manager_phone": acc.manager_phone,
        "manager_email": acc.manager_email,
    }


@router.post("/escalate", response_model=EscalateResponse)
def escalate_to_human(
    payload: EscalateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Escalates the conversation to a human attendant."""
    now = datetime.now(timezone.utc)
    is_business_hours = 8 <= now.hour < 20 and now.weekday() < 5
    if not is_business_hours:
        return EscalateResponse(
            session_id=f"SES{uuid.uuid4().hex[:6].upper()}",
            status="outside_hours",
            estimated_wait_minutes=0,
            message="Human support is available Monday to Friday, from 8h to 20h. Please leave a message for your manager or open a ticket.",
        )
    wait = 5 if payload.priority == "urgent" else 15
    return EscalateResponse(
        session_id=f"SES{uuid.uuid4().hex[:6].upper()}",
        status="queued",
        estimated_wait_minutes=wait,
        message=f"You will be attended in approximately {wait} minutes. A human attendant will join the chat shortly.",
    )


@router.get("/faq", response_model=FAQResponse)
def get_faq(
    query: str = Query(..., description="User question"),
    category: Optional[str] = Query(None),
    _: dict = Depends(get_current_user),
):
    """Searches the FAQ database for answers."""
    ql = query.lower()
    best = None
    best_score = 0
    for item in FAQ_DATA:
        if category and item["category"] != category:
            continue
        keywords = item.get("query_keywords", [])
        score = sum(1 for kw in keywords if kw in ql)
        if score > best_score:
            best_score = score
            best = item
    if not best:
        return FAQResponse(query=query, category="general", answer="I couldn't find a specific answer. Try rephrasing or contact your manager.", confidence=0.0)
    return FAQResponse(query=query, category=best["category"], answer=best["answer"], confidence=min(1.0, best_score * 0.4))


@router.get("/branch", response_model=BranchInfoOut)
def get_branch_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Returns details about the user's physical branch."""
    acc = _get_account(current_user["account_id"], db)
    return BranchInfoOut(
        account_id=acc.id, branch_name=acc.branch_name,
        address=acc.branch_address, phone=acc.branch_phone,
        opening_hours="Monday to Friday, 10h to 16h",
        manager_name=acc.manager_name, manager_phone=acc.manager_phone, manager_email=acc.manager_email,
    )
