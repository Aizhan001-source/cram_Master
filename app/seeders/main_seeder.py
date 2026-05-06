import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_access.db.session import AsyncSessionLocal

from seeders.role_seeder import seed_roles
from seeders.education_seeder import seed_educations
from seeders.subject_seeder import seed_subjects
from seeders.user_seeder import seed_users
from seeders.student_seeder import seed_students
from seeders.tutor_seeder import seed_tutors
from seeders.courses_seeder import seed_courses
from seeders.schedule_seeder import seed_schedules
from seeders.booking_seeder import seed_bookings
from seeders.payment_seeder import seed_payments
from seeders.review_seeder import seed_reviews
from seeders.favorite_seeder import seed_favorites


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