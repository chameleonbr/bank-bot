from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    category = Column(String, nullable=False)       # transferencia | investimento | credito | outros
    description = Column(String, nullable=False)
    priority = Column(String, default="normal")     # low | normal | high | urgent
    status = Column(String, default="open")         # open | in_progress | resolved | closed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolution = Column(String, default="")

    account = relationship("Account", back_populates="tickets")
