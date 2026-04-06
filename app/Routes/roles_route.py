from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.access_control import fds_roles
from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models import Role
from app.Schema.role_schema import RolesEnum

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
def get_roles_list(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [{"id": r.id, "name": r.name, "description": r.description} for r in roles]
