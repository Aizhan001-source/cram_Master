from fastapi import HTTPException, status
from uuid import UUID

from data_access.db.models.student import Student


class StudentService:
    def __init__(self, repository):
        self.repository = repository

    async def create_student(self, user_id: UUID) -> Student:
        existing = await self.repository.get_by_user_id(user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already exists"
            )

        return await self.repository.create(user_id)

    async def get_student(self, student_id: UUID) -> Student:
        student = await self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return student

    async def get_all_students(self) -> list[Student]:
        return await self.repository.get_all()

    async def delete_student(self, student_id: UUID):
        student = await self.get_student(student_id)
        await self.repository.delete(student)