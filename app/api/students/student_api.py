from fastapi import APIRouter, Depends, status, HTTPException
from uuid import UUID
from business_logic.students.student_service import StudentService
from api.students.student_schemas import StudentCreate, StudentRead
from utils.auth_middleware import get_current_user
from data_access.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

def get_student_service(db: AsyncSession = Depends(get_db)) -> StudentService:
    return StudentService(db)

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    current_user=Depends(get_current_user()),
    service: StudentService = Depends(get_student_service),
):
    return await service.create_student(current_user.id)


@router.get("/", response_model=list[StudentRead])
async def get_students(
    service: StudentService = Depends(get_student_service),
):
    return await service.get_all_students()


@router.get("/me", response_model=StudentRead)
async def get_my_student(
    current_user=Depends(get_current_user()),
    service: StudentService = Depends(get_student_service),
):
    student = await service.get_student(current_user.id)  # FIX
    if not student:
        return await service.create_student(current_user.id)
    return student


@router.get("/count")
async def get_students_count(
    service: StudentService = Depends(get_student_service),
):
    return await service.get_students_count()


@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id(
    student_id: UUID,
    service: StudentService = Depends(get_student_service),
):
    return await service.get_student(student_id)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: UUID,
    service: StudentService = Depends(get_student_service),
):
    student = await service.get_student(student_id)
    await service.delete(student)