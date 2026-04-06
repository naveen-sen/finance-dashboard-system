from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.access_control import fds_roles
from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models.transaction_model import Transaction
from app.Schema.role_schema import RolesEnum
from app.Schema.transaction_schema import TransactionCreate, TransactionUpdate
from app.Services.transaction_service import (
    create_transaction_service,
    get_transaction_service,
    get_user_transactions_service,
    update_transaction_service,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/")
@fds_roles([RolesEnum.ANLST, RolesEnum.ADMIN])
def read_transactions(
    skip: int = 0,
    limit: int = Query(10, le=50),
    category: Optional[str] = None,
    typeof: Optional[str] | None = Query(default=None, alias='type'),
    date: Optional[datetime] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transactions = get_user_transactions_service(
        current_user, db, skip=skip, limit=limit, category=category, typeof=typeof, date=date
    )
    return transactions


@router.post("/")
@fds_roles([RolesEnum.ADMIN])
def create_transaction(
    transaction: TransactionCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        new_transaction = create_transaction_service(
            db, **transaction.dict(), user_payload=current_user
        )
        return new_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{transaction_id}")
@fds_roles([RolesEnum.ADMIN])
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        updated = update_transaction_service(
            transaction_id, **transaction_update.dict(), user_payload=current_user, db=db
        )
        return updated
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{transaction_id}")
@fds_roles([RolesEnum.ADMIN])
def delete_transaction(
    transaction_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    transaction = get_transaction_service(transaction_id, current_user, db)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted"}
