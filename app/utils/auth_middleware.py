from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from data_access.db.session import get_db
from business_logic.users.user_service import UserService
from utils.token_creator import decode_access_token
from api.users.user_schemas import CurrentUser

security = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_current_user(required_roles: list[str] | None = None):
    async def _get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_service: UserService = Depends(get_user_service),
    ) -> CurrentUser:

        try:
            payload = decode_access_token(credentials.credentials)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        role_name = await user_service.get_user_role_by_user_id(UUID(user_id))

        if not role_name:
            raise HTTPException(status_code=401, detail="User not found")

        # role check
        if required_roles and role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return CurrentUser(
            id=UUID(user_id),
            role=role_name
        )

    return _get_current_user