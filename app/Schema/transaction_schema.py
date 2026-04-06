from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.Models.transaction_model import TransactionTypeEnum


class TransactionBase(BaseModel):
    amount: float
    type: TransactionTypeEnum
    category: str
    description: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    amount: float
    type: TransactionTypeEnum  # 'income' or 'expense'
    category: str
    description: Optional[str] = None


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
