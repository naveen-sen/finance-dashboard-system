from typing import ClassVar

from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    pass


class PrimaryKey(SQLModel):
    id: int = Field(default=None, nullable=False, primary_key=True)
