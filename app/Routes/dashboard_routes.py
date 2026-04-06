from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.access_control import fds_roles
from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models import User
from app.Schema.dashboard_schema import DashboardSummary
from app.Schema.role_schema import RolesEnum
from app.Services.dashboard_service import get_dashboard_summary as get_dashboard_summary_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
@fds_roles([RolesEnum.ANLST, RolesEnum.ADMIN])
def dashboard_summary(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_dashboard_summary_service(current_user, db)
