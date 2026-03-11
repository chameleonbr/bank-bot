from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    name = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    bank = Column(String, default="")
    bank_code = Column(String, default="")
    agency = Column(String, default="")
    account_number = Column(String, default="")
    pix_key = Column(String, default="")
    alias = Column(String, default="")

    account = relationship("Account", back_populates="contacts")
