from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from data_access.db.models.student import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID) -> Student:
<<<<<<< HEAD
        student = Student(user_id=user_id)

        self.session.add(student)

        await self.session.flush()

=======
        student = Student(id=user_id)
        self.session.add(student)
        await self.session.flush()
>>>>>>> 7431d622914a6d09f8e134a327ab5906690e013e
        return student

    async def get_by_id(self, student_id: UUID):
        result = await self.session.execute(
            select(Student)
            .where(Student.id == student_id)
            .options(selectinload(Student.user))
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(
            select(Student).options(selectinload(Student.user))
        )
        return result.scalars().all()

    async def delete(self, student: Student):
        await self.session.delete(student)
        await self.session.commit()

    async def get_count(self) -> int:
        result = await self.session.execute(select(func.count(Student.id)))
        return result.scalar_one()