from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field

from app.db.base import Base, PrimaryKey


class TransactionTypeEnum(str, Enum):
    Income = 'Income'
    Expense = 'Expense'


class Transaction(Base, PrimaryKey, table=True):
    amount: float = Field(nullable=False)
    type: TransactionTypeEnum
    category: str = Field(nullable=False)
    date: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.utcnow
    )
    description: Optional[str] = Field(default=None, max_length=500)
    user_id: int = Field(foreign_key="user.id")
