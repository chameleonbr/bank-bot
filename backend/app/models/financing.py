from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Financing(Base):
    __tablename__ = "financings"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    modality = Column(String, nullable=False)           # imovel | veiculo | rural
    asset_value = Column(Float, nullable=False)
    financed_amount = Column(Float, nullable=False)
    entry_value = Column(Float, nullable=False)
    outstanding_balance = Column(Float, nullable=False)
    installment_amount = Column(Float, nullable=False)
    num_installments = Column(Integer, nullable=False)
    paid_installments = Column(Integer, default=0)
    amortization_system = Column(String, default="SAC")  # SAC | PRICE | MISTO
    monthly_rate = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    next_due_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")           # active | pending | analysis | paid

    account = relationship("Account", back_populates="financings")
