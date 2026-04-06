from enum import Enum
from functools import wraps
from typing import Any, Callable, List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.user import get_current_user
from app.db.session import get_db
from app.Schema.role_schema import RolesEnum
from app.Services.user_service import get_user_roles, has_role
from app.utils.constants import OPERATION_NOT_PERMITTED


def fds_roles(required_roles: List[RolesEnum]):
    required_roles_ids = [r.value for r in required_roles]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def inner(
            current_user: dict = Depends(get_current_user),
            db: Session = Depends(get_db),
            *args: Any,
            **kwargs: Any
        ) -> Any:
            user_id = current_user.get("id") if isinstance(current_user, dict) else None
            if user_id is None:
                raise HTTPException(status_code=401, detail='User not authorised')
            user_roles_data = get_user_roles(db, user_id)
            user_role_ids = [r['id'] for r in user_roles_data]  # type: ignore
            if not any(role_id in user_role_ids for role_id in required_roles_ids):
                raise HTTPException(status_code=403, detail=OPERATION_NOT_PERMITTED)
            return func(*args, **kwargs, current_user=current_user, db=db)

        return inner

    return decorator
