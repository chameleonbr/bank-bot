from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    loan_type = Column(String, nullable=False)      # pessoal | consignado | empresarial
    requested_amount = Column(Float, nullable=False)
    outstanding_balance = Column(Float, nullable=False)
    installment_amount = Column(Float, nullable=False)
    num_installments = Column(Integer, nullable=False)
    paid_installments = Column(Integer, default=0)
    monthly_rate = Column(Float, nullable=False)    # e.g. 0.0199
    start_date = Column(DateTime, nullable=False)
    next_due_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")       # active | paid | pending_approval | analysis

    account = relationship("Account", back_populates="loans")
