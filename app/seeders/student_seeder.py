from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.models.student import Student
from data_access.db.models.user import User
from data_access.db.models.role import Role


async def seed_students(db: AsyncSession):
    # Получаем роль student
    role_result = await db.execute(
        select(Role).where(Role.name == "student")
    )
    student_role = role_result.scalar_one_or_none()

    if not student_role:
        raise Exception("Role 'student' not found")

    # Получаем всех пользователей с этой ролью
    users_result = await db.execute(
        select(User).where(User.role_id == student_role.id)
    )
    users = users_result.scalars().all()

    for user in users:
        # Проверяем, есть ли уже студент
        exists = await db.execute(
            select(Student).where(Student.user_id == user.id)
        )

        if exists.scalar_one_or_none():
            continue

        db.add(Student(user_id=user.id))

    await db.commit()
    print("Students seeded!")