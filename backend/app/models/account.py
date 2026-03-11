from sqlalchemy import Column, String, Float, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True)           # ACC001 .. ACC004
    holder_name = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    account_type = Column(String, default="PF")     # PF | PJ
    investor_profile = Column(String, default="conservador")  # conservador | moderado | arrojado
    credit_score = Column(Float, default=700.0)
    balance_checking = Column(Float, default=0.0)
    balance_savings = Column(Float, default=0.0)
    balance_salary = Column(Float, default=0.0)
    manager_name = Column(String, default="")
    manager_phone = Column(String, default="")
    manager_email = Column(String, default="")
    branch_name = Column(String, default="Agência Centro")
    branch_address = Column(String, default="")
    branch_phone = Column(String, default="")

    @property
    def account_id(self) -> str:
        return self.id

    user = relationship("User", back_populates="account", uselist=False)
    transactions = relationship("Transaction", back_populates="account")
    contacts = relationship("Contact", back_populates="account")
    pix_keys = relationship("PixKey", back_populates="account")
    scheduled_ops = relationship("ScheduledOperation", back_populates="account")
    investments = relationship("Investment", back_populates="account")
    loans = relationship("Loan", back_populates="account")
    financings = relationship("Financing", back_populates="account")
    tickets = relationship("Ticket", back_populates="account")
