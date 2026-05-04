# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from business_logic.users.user_service import UserService
# from data_access.users.user_repository import UserRepository
# from utils.token_creator import decode_access_token
# from sqlalchemy.ext.asyncio import AsyncSession
# from data_access.db.session import get_db
# from uuid import UUID

# security = HTTPBearer()

# def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
#     return UserService(db)

# def get_current_user(required_roles: list[str] | None = None):
#     async def _get_user(
#         credentials: HTTPAuthorizationCredentials = Depends(security),
#         user_service: UserService = Depends(get_user_service),
#     ):
#         token = credentials.credentials

#         try:
#             payload = decode_access_token(token)  # payload должен содержать user_id
#         except Exception:
#             raise HTTPException(status_code=401, detail="Invalid or expired token")

#         user_id = payload.get("sub")
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token payload")

#         # получаем роль из БД
#         role_name = await user_service.get_user_role_by_user_id(UUID(user_id))
#         print("ADSAdDDAADADDADA", role_name)
        
#         if required_roles and role_name not in required_roles:
#             raise HTTPException(status_code=403, detail="Not enough permissions")

#         return {"user_id": user_id, "role": role_name, **payload}
#     return _get_user

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.token_creator import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.session import get_db
from business_logic.users.user_service import UserService
from uuid import UUID
from api.users.user_schemas import CurrentUser

security = HTTPBearer()

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_current_user(required_roles: list[str] | None = None):
    async def _get_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        user_service: UserService = Depends(get_user_service),
    ):
        token = credentials.credentials

        try:
            payload = decode_access_token(token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="No user id in token")

        role_name = await user_service.get_user_role_by_user_id(UUID(user_id))

        if required_roles and role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        return {
            "user_id": user_id,
            "role": role_name,
            "email": payload.get("email"),
        }

    return _get_user