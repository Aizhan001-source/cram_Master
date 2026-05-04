import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal

from .role_seeder import seed_roles
from .education_seeder import seed_educations
from .subject_seeder import seed_subjects

from .user_seeder import seed_users
from .student_seeder import seed_students
from .tutor_seeder import seed_tutors

from .courses_seeder import seed_courses
from .schedule_seeder import seed_schedules

from .booking_seeder import seed_bookings
from .payment_seeder import seed_payments

from .review_seeder import seed_reviews
from .favorite_seeder import seed_favorites


async def main():
    async with AsyncSessionLocal() as db:
        try:
            print("\n🚀 START SEEDING\n")

            # 1. BASE TABLES
            print("➡️ roles")
            await seed_roles(db)

            print("➡️ educations")
            await seed_educations(db)

            print("➡️ subjects")
            await seed_subjects(db)

            # 2. USERS
            print("➡️ users")
            await seed_users(db)

            print("➡️ students")
            await seed_students(db)

            print("➡️ tutors")
            await seed_tutors(db)

            # 3. COURSES
            print("➡️ courses")
            await seed_courses(db)

            # 4. SCHEDULES
            print("➡️ schedules")
            await seed_schedules(db)

            # 5. BOOKINGS
            print("➡️ bookings")
            await seed_bookings(db)

            # 6. PAYMENTS
            print("➡️ payments")
            await seed_payments(db)

            # 7. REVIEWS
            print("➡️ reviews")
            await seed_reviews(db)

            # 8. FAVORITES
            print("➡️ favorites")
            await seed_favorites(db)

            print("\n✅ ALL SEEDERS COMPLETED SUCCESSFULLY\n")

        except Exception as e:
            print("\n❌ SEEDING FAILED:")
            print(f"Error: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())