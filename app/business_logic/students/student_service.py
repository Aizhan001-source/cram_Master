from fastapi import HTTPException


class StudentService:
    def __init__(self, repository):
        self.repository = repository

    async def create_student(self, user_id):
        existing = await self.repository.get_by_user_id(user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Student already exists")

        return await self.repository.create(user_id)

    async def get_student(self, student_id):
        student = await self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    async def get_all_students(self):
        return await self.repository.get_all()