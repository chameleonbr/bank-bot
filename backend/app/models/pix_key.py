from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class PixKey(Base):
    __tablename__ = "pix_keys"

    id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    key_type = Column(String, nullable=False)   # cpf | cnpj | email | phone | random
    key_value = Column(String, nullable=False)
    status = Column(String, default="active")   # active | pending | deleted

    account = relationship("Account", back_populates="pix_keys")


class PixLimit(Base):
    __tablename__ = "pix_limits"

    account_id = Column(String, ForeignKey("accounts.id"), primary_key=True)
    limit_daytime = Column(Float, default=5000.0)     # 06h–22h
    limit_nighttime = Column(Float, default=1000.0)   # 22h–06h
