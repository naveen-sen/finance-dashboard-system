from typing import Dict, cast

from sqlalchemy import case, desc, false, func, true
from sqlalchemy.orm import Session
from sqlalchemy.sql import ColumnElement

from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models.transaction_model import Transaction
from app.Schema.dashboard_schema import (
    CategoryTotal,
    DashboardSummary,
    MonthlyTrend,
    RecentActivity,
)


def get_dashboard_summary(user_payload: dict, db: Session) -> DashboardSummary:
    user_id = user_payload["id"]

    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.type == 'Income').scalar() or 0.0  # type: ignore

    total_expense = (
        db.query(func.sum(Transaction.amount))
        .filter((Transaction.user_id == user_id) & (Transaction.type == 'Expense'))
        .scalar()
        or 0.0
    )

    net_balance = total_income - total_expense

    # # Category Wise Total

    category_wise_query = db.query(Transaction.category, Transaction.type, func.sum(Transaction.amount).label('total')).filter(Transaction.user_id == user_id).group_by(Transaction.category, Transaction.type).all()  # type: ignore

    category_totals: Dict[str, CategoryTotal] = {}
    for cat, typ, amt in category_wise_query:
        if cat not in category_totals:
            category_totals[cat] = CategoryTotal()
        if typ == "Income":
            category_totals[cat].income = float(amt or 0)
        else:
            category_totals[cat].expenses = float(amt or 0)

    # Recent activity (last 10)
    recent_transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(desc(cast(ColumnElement, Transaction.date)))
        .limit(10)
        .all()
    )

    recent_activity = [
        RecentActivity(
            id=t.id,
            amount=t.amount,
            type=t.type.value if hasattr(t.type, 'value') else t.type,
            category=t.category,
            date=t.date.date(),
            description=t.description,
        )
        for t in recent_transactions
    ]

    # Monthly trends (last 12 months)
    trends_query = (
        db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.sum(case((Transaction.type == 'Income', Transaction.amount), else_=0)).label('income'),  # type: ignore
            func.sum(case((Transaction.type == 'Expense', Transaction.amount), else_=0)).label('expenses'),  # type: ignore
            func.sum(case((Transaction.type == 'Income', Transaction.amount), else_=-Transaction.amount)).label('net'),  # type: ignore
        )
        .filter(Transaction.user_id == user_id)
        .group_by('month')
        .order_by(desc('month'))
        .limit(12)
        .all()
    )

    monthly_trends = [
        MonthlyTrend(
            month=row.month,
            income=float(row.income or 0),
            expenses=float(row.expenses or 0),
            net=float(row.net or 0),
        )
        for row in trends_query
    ]

    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expense,
        net_balance=net_balance,
        category_totals=category_totals,
        recent_activity=recent_activity,
        monthly_trends=monthly_trends,
    )
