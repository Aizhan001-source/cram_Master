from fastapi import Depends, HTTPException
from api.users.user_schemas import UserAllRead, UserLoginResponse, UserProfileRead, UserRead
from data_access.db.session import get_db
from data_access.users.user_repository import UserRepository
from uuid import UUID
import hashlib
from utils.token_creator import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from utils.password_hasher import hash_password
from data_access.tutors.tutor_repository import TutorRepository
from data_access.students.student_repository import StudentRepository
from sqlalchemy import select
from data_access.db.models.role import Role

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)
        self.tutor_repo = TutorRepository(db)
        self.student_repo = StudentRepository(db)

<<<<<<< HEAD
    async def _get_role_name(self, role_id):
=======
    async def _get_role_name(self, role_id: UUID):
>>>>>>> 7431d622914a6d09f8e134a327ab5906690e013e
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        role = result.scalar_one_or_none()
<<<<<<< HEAD
        return role.name if role else None

    async def register_user(
        self,
        first_name,
        last_name,
        email,
        password,
        role_id,
        education_id=None
    ):

=======

        if not role:
            raise HTTPException(400, "Invalid role_id")  # 🔥 ВАЖНО

        return role.name

    async def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        role_id: UUID,
        education_id: UUID | None = None
    ):

        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(400, "Email already registered")

>>>>>>> 7431d622914a6d09f8e134a327ab5906690e013e
        hashed = hash_password(password)

        user = await self.repo.create_user(
            first_name,
            last_name,
            email,
            hashed,
            role_id
        )

        role_name = await self._get_role_name(role_id)

        if role_name == "tutor":
            if not education_id:
                raise HTTPException(400, "education_id is required for tutor")

            await self.tutor_repo.create_tutor(user.id, education_id)

        elif role_name == "student":
            await self.student_repo.create(user.id)

        await self.db.commit()

        return user
            
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