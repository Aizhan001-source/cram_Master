from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from data_access.db.models.student import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID) -> Student:
        student = Student(user_id=user_id)
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def get_by_id(self, student_id: UUID) -> Student | None:
        return await self.session.get(Student, student_id)

    async def get_all(self) -> list[Student]:
        result = await self.session.execute(select(Student))
        return result.scalars().all()

    async def get_by_user_id(self, user_id: UUID) -> Student | None:
        result = await self.session.execute(
            select(Student).where(Student.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, student: Student):
        await self.session.delete(student)
        await self.session.commit()