from enum import Enum
from typing import cast

from sqlmodel import SQLModel

from app.Schema.permission_schema import Permission
from app.Schema.user_schema import User


class RoleResponse(SQLModel):
    id: int
    name: str
    category: str | None = None
    users: list[User]


class RolesEnum(int, Enum):
    permissions: list[Permission] | None

    def __new__(cls, value: int, permissions: list[Permission] | None = None) -> "RolesEnum":
        obj = int.__new__(cls, value)
        obj = cast("RolesEnum", obj)
        obj._value_ = value
        obj.permissions = permissions
        return obj

    def get_permissions(self) -> list[str]:
        if self.permissions:
            return [permission.value for permission in self.permissions]
        return []

    VWR = (1, [Permission.VIEWER])
    ANLST = (2, [Permission.ANALYST])
    ADMIN = (3, [Permission.ADMIN])
