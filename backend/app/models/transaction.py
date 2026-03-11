from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)          # negative = debit, positive = credit
    category = Column(String, default="outros")
    type = Column(String, default="debit")          # debit | credit | pix | ted | transfer
    counterpart_name = Column(String, default="")
    counterpart_key = Column(String, default="")
    receipt_id = Column(String, default="")
    status = Column(String, default="completed")    # completed | pending | failed

    account = relationship("Account", back_populates="transactions")
