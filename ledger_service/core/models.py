from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True)
    app_id = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False, unique=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LedgerRequest(BaseModel):
    app_id: str
    operation: str
    owner_id: str
    nonce: str
