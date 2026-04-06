from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db_session  # optional
from app.Models import Role, User, UserRole
from app.utils.constants import Admin, Analyst, Viewer


def seed_roles(db: Session):
    roles = [
        Role(name=Viewer, description='Can only view dashboard data'),  # type: ignore
        Role(name=Analyst, description='Can view records and access insights'),  # type: ignore
        Role(name=Admin, description='Can create, update, manage records and users'),  # type: ignore
    ]
    for role in roles:
        existing = db.query(Role).filter(Role.name == role.name).first()  # type: ignore
        if not existing:
            db.add(role)
    db.commit()


def get_user_roles(db: Session, user_id: int) -> List[str]:
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).join(Role).all()  # type: ignore
    return [{"id": ur.role.id, "name": ur.role.name} for ur in user_roles]  # type: ignore


def set_user_active(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()  # type: ignore
    if user:
        user.is_active = is_active
        db.commit()
        return True
    return False


def has_role(user_roles: List[str], required_role: str) -> bool:
    return required_role in user_roles


def get_user_role(user_id: int, role_id: int, db: Session):
    user_role = db.query(UserRole).join(Role).filter(UserRole.user_id == user_id, Role.id == role_id).first()  # type: ignore
    if not user_role:
        raise HTTPException(404, 'Role Not Found')
    db.delete(user_role)
    db.commit()
    return f'Role Removed Successfully for User Id {user_id}'
