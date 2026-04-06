from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship

from app.db.base import Base, PrimaryKey


class UserRole(Base, PrimaryKey, table=True):
    user_id: int = Field(foreign_key='user.id', ondelete='CASCADE')

    role_id: int = Field(foreign_key='role.id')

    user: 'User' = Relationship(back_populates='user_roles')  # type: ignore
    role: 'Role' = Relationship(back_populates='user_roles')  # type: ignore
