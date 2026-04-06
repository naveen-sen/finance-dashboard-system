from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.auth.access_control import fds_roles
from app.auth.user import get_current_user
from app.db.session import get_db
from app.Models import Role, User, UserRole
from app.Schema.role_schema import RolesEnum
from app.Services.user_service import get_user_role, get_user_roles
from app.Services.user_service import seed_roles as seed_user_roles
from app.Services.user_service import set_user_active

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_active == True, User.deleted == False).all()  # type: ignore
    return [
        {"id": u.id, "name": u.name, "email": u.email, "roles": get_user_roles(db, u.id)}
        for u in users
    ]


@router.get("/{user_id}")
def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()  # type: ignore
    if not user:
        raise HTTPException(404, "User not found")
    roles = get_user_roles(db, user_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_active": user.is_active,
        "roles": roles,
    }


@router.post("/{user_id}/roles/{role_id}")
def add_role_to_user(
    role_id: int,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = db.query(Role).filter(Role.id == role_id).first()  # type: ignore
    if not role:
        raise HTTPException(404, "Role not found")
    existing_link = db.query(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role.id).first()  # type: ignore
    if not existing_link:
        user_role = UserRole(user_id=user_id, role_id=role.id)  # type: ignore
        db.add(user_role)
        db.commit()
    return {"message": f"Role {role.name} assigned to user {user_id}"}


@router.put("/{user_id}/active")
@fds_roles([RolesEnum.ADMIN])
def update_user_active(
    is_active: bool,
    current_user: User = Depends(get_current_user),
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    success = set_user_active(db, user_id, is_active)
    if not success:
        raise HTTPException(404, "User not found")
    return {"message": f"User {user_id} status updated to {'active' if is_active else 'inactive'}"}


@router.post("/seed-roles")
@fds_roles([RolesEnum.ADMIN])
def seed_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    seed_user_roles(db)
    return {"message": "Roles seeded"}


@router.get("/get_user_roles/{user_id}")
def get_user_role_list(
    user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    user_roles = get_user_roles(db, user_id)
    if not user_roles:
        raise HTTPException(404, 'User Role Not found')
    return user_roles


@router.delete('/delete-access/{user_id}/{role_id}')
def remove_user_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_role = get_user_role(user_id, role_id, db)
    return user_role
