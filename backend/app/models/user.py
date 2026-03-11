from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # e.g. USR001
    account_id = Column(String, ForeignKey("accounts.id"), unique=True, nullable=False)
    pin_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    account = relationship("Account", back_populates="user")
