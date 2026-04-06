from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from app.db.base import Base, PrimaryKey
from app.Models.role_model import Role
from app.Models.user_role_model import UserRole


class User(Base, PrimaryKey, table=True):
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    deleted: bool = Field(default=False)
    is_active: bool = Field(default=True)
    password: str = Field(nullable=False)

    user_roles: list[UserRole] = Relationship(
        back_populates='user',
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'dynamic'},
    )

    roles: list[Role] = Relationship(back_populates="users", link_model=UserRole)

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'
