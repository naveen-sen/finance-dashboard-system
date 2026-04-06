from pydantic import Field
from sqlmodel import SQLModel

from app.utils.base_config import BaseConfigSchema


class UserBase(BaseConfigSchema):
    email: str
    first_name: str | None = Field(default=None, alias='firstName')
    last_name: str | None = Field(default=None, alias='lastName')


class User(SQLModel):
    id: int
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class UserResponse(UserBase):
    id: int
