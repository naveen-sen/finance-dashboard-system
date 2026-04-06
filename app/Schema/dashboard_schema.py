from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel


class CategoryTotal(BaseModel):
    income: float = 0.0
    expenses: float = 0.0


class MonthlyTrend(BaseModel):
    month: str  # 'YYYY-MM'
    income: float = 0.0
    expenses: float = 0.0
    net: float = 0.0


class RecentActivity(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    description: Optional[str] = None


class DashboardSummary(BaseModel):
    total_income: float = 0.0
    total_expenses: float = 0.0
    net_balance: float = 0.0
    category_totals: Dict[str, CategoryTotal] = {}
    recent_activity: List[RecentActivity] = []
    monthly_trends: List[MonthlyTrend] = []
