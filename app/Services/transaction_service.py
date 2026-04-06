from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Depends
from sqlalchemy import Date, case, extract, func
from sqlalchemy.orm import Session

from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models import User
from app.Models.transaction_model import Transaction, TransactionTypeEnum


def create_transaction_service(
    db: Session,
    amount: float,
    type: TransactionTypeEnum,
    category: str,
    description: Optional[str],
    user_payload: dict,
):
    user_id = user_payload["id"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise ValueError("User not active")
    transaction = Transaction(
        amount=amount, type=type, category=category, description=description, user_id=user_id
    )  # type: ignore
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def get_user_transactions_service(
    user_payload: dict,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    typeof: Optional[str] = None,
    date: Optional[datetime] = None,
) -> List[Transaction]:
    user_id = user_payload["id"]
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if category:
        query = query.filter(Transaction.category == category)  # type: ignore

    if typeof:
        query = query.filter(Transaction.type == typeof)  # type: ignore

    if date:
        query = query.filter(Transaction.date.cast(Date) == date.date())  # type: ignore

        print(date, type(date))

    return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()  # type: ignore


def get_transaction_service(transaction_id: int, user_payload: dict, db: Session = Depends(get_db)):
    user_id = user_payload["id"]
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id, Transaction.id == transaction_id)  # type: ignore
        .first()
    )


def update_transaction_service(
    transaction_id: int,
    amount: Optional[float],
    type: Optional[TransactionTypeEnum],
    category: Optional[str],
    description: Optional[str],
    user_payload: dict,
    db: Session = Depends(get_db),
):
    transaction = get_transaction_service(transaction_id, user_payload, db)
    if not transaction:
        raise ValueError("Transaction not found")
    if amount is not None:
        transaction.amount = amount
    if type is not None:
        transaction.type = type
    if category is not None:
        transaction.category = category
    if description is not None:
        transaction.description = description
    db.commit()
    db.refresh(transaction)
    return transaction
