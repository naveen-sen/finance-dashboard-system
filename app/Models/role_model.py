from typing import List

from sqlmodel import Field, Relationship, SQLModel

from app.db.base import Base, PrimaryKey
from app.Models.user_role_model import UserRole


class Role(Base, PrimaryKey, table=True):
    name: str = Field(unique=True, max_length=50, index=True, nullable=False)
    description: str = Field(nullable=False)

    user_roles: List[UserRole] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "select"},
    )
    users: List["User"] = Relationship(  # type: ignore
        back_populates="roles", link_model=UserRole, sa_relationship_kwargs={"lazy": "select"}
    )
