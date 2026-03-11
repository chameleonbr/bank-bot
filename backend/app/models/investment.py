from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Investment(Base):
    __tablename__ = "investments"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    product_type = Column(String, nullable=False)   # CDB | LCI | LCA | TESOURO | FUNDO | POUPANCA
    product_name = Column(String, nullable=False)
    amount_invested = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    rate = Column(String, default="")               # e.g. "90% CDI"
    start_date = Column(DateTime, nullable=False)
    maturity_date = Column(DateTime, nullable=True)
    liquidity = Column(String, default="no_vencimento")  # diaria | no_vencimento | D+1 | D+30
    status = Column(String, default="active")       # active | redeemed

    account = relationship("Account", back_populates="investments")
