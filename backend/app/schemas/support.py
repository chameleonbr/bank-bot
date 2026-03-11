from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class OpenTicketRequest(BaseModel):
    category: str
    description: str
    priority: str = "normal"


class TicketOut(BaseModel):
    id: str
    category: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolution: str

    model_config = {"from_attributes": True}


class ScheduleManagerCallRequest(BaseModel):
    preferred_date: str   # YYYY-MM-DD
    preferred_time: str   # HH:MM
    subject: str


class SendManagerMessageRequest(BaseModel):
    message: str
    category: str = "geral"


class ManagerCallResponse(BaseModel):
    confirmation_id: str
    manager_name: str
    scheduled_date: str
    scheduled_time: str
    subject: str
    message: str


class EscalateRequest(BaseModel):
    reason: str
    priority: str = "normal"


class EscalateResponse(BaseModel):
    session_id: str
    status: str
    estimated_wait_minutes: int
    message: str


class FAQResponse(BaseModel):
    query: str
    category: str
    answer: str
    confidence: float


class BranchInfoOut(BaseModel):
    account_id: str
    branch_name: str
    address: str
    phone: str
    opening_hours: str
    manager_name: str
    manager_phone: str
    manager_email: str
