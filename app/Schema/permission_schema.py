from enum import Enum

from app.utils.constants import Admin, Analyst, Viewer


class Permission(str, Enum):
    VIEWER = Viewer
    ANALYST = Analyst
    ADMIN = Admin
