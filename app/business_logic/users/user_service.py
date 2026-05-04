from fastapi import Depends, HTTPException
from api.users.user_schemas import UserAllRead, UserLoginResponse, UserProfileRead, UserRead
from data_access.db.session import get_db
from data_access.users.user_repository import UserRepository
from uuid import UUID
import hashlib
from utils.token_creator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from utils.password_hasher import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register_user(self, first_name, last_name, email, password, role_id):
        created_user = await self.repo.register_user(
            first_name,
            last_name,
            email,
            hash_password(password),
            role_id
        )

        return UserRead(
            id=created_user.id,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            email=created_user.email,
        )

    async def login_user(self, email, password):
        hashed_password = hash_password(password)
        
        logged_in_user = await self.repo.login_user(email, hashed_password)
        
        if not logged_in_user:
            return None  # или raise HTTPException(401)

        # создаем JWT
        token_data = {"sub": str(logged_in_user.id), "email": logged_in_user.email}
        access_token = create_access_token(token_data)

        return {
            "user": UserRead(
                id=logged_in_user.id,
                first_name=logged_in_user.first_name,
                last_name=logged_in_user.last_name,
                email=logged_in_user.email
            ),
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def get_all_users(self):
        all_users = await self.repo.get_all_users()
        
        return [
            UserAllRead.model_validate(user)
            for user in all_users
        ]

    async def get_user_role_by_user_id(self, user_id) -> str:
        return await self.repo.get_user_role_by_user_id(user_id)
    
    async def get_user_profile(self, user_id):
        user = await self.repo.get_user_profile(user_id)
        
        if not user:
            return None
        
        return UserProfileRead(
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
        )