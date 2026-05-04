import asyncio, sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal
from user_seeder import seed_users
from role_seeder import seed_roles
from education_seeder import seed_educations
from tutor_seeder import seed_tutors
from payment_seeder import seed_payments
from booking_seeder import seed_bookings
from favorite_seeder import seed_favorites
from courses_seeder import seed_courses
from payment_seeder import seed_payments
from subject_seeder import seed_subjects
from review_seeder import seed_reviews
from student_seeder import seed_students
from schedule_seeder import seed_schedules




async def main():
    async with AsyncSessionLocal() as db:

        # 1. базовые сущности
        # await seed_roles(db)
        # await seed_users(db)
        # await seed_educations(db)

        # 2. преподаватели и студенты
        # await seed_tutors(db)
        # await seed_students(db)   

        # 3. предметы и курсы
        await seed_subjects(db)
        await seed_courses(db)

        # 4. расписание
        await seed_schedules(db)

        # 5. бронирования
        await seed_bookings(db)

        # 6. платежи
        await seed_payments(db)

        # 7. остальное
        await seed_favorites(db)
        await seed_reviews(db)


if __name__ == "__main__":
    asyncio.run(main())

