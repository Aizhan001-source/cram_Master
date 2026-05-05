from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from sqlalchemy.orm import selectinload
from data_access.db.models.role import Role
from data_access.db.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        hashed_password: str,
        role_id
    ) -> User:

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hashed_password,
            role_id=role_id,
        )

        self.db.add(user)

        # важно: чтобы user.id сразу появился
        await self.db.flush()

        return user

    async def login_user(self, email, hashed_password):
        result = await self.db.execute(
            select(User).where(
                User.email == email,
                User.password_hash == hashed_password
            )
        )

        return result.scalar_one_or_none()
    
    async def get_all_users(self):
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
        )

        users = result.scalars().all()
        return users

    async def get_user_role_by_user_id(self, user_id: UUID) -> str | None:
        print("ADSDDADADADAD", user_id)
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )

        user = result.scalar_one_or_none()
        # print("AADSDASDASDAS", user, user.role)
        if user and user.role:
            return user.role.name
        return None
    
    async def get_user_profile(self, user_id: UUID) -> User | None:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        return user
    
    async def get_by_id(self, user_id: UUID):
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()