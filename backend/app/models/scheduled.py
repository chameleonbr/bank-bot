from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ScheduledOperation(Base):
    __tablename__ = "scheduled_operations"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    type = Column(String, nullable=False)           # pix | ted | payment
    amount = Column(Float, nullable=False)
    destination_name = Column(String, default="")
    destination_key = Column(String, default="")
    schedule_datetime = Column(DateTime, nullable=False)
    recurrence = Column(String, default="none")     # none | weekly | monthly
    status = Column(String, default="scheduled")    # scheduled | cancelled | executed

    account = relationship("Account", back_populates="scheduled_ops")
