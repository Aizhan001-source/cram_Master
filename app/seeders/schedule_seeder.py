from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from data_access.db.models.schedule import Schedule
from data_access.db.models.course import Course


async def seed_schedules(db: AsyncSession):
    courses = (await db.execute(select(Course))).scalars().all()

    if not courses:
        print("No courses found")
        return

    now = datetime.utcnow()

    for i, course in enumerate(courses):
        result = await db.execute(
            select(Schedule).where(Schedule.course_id == course.id)
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                Schedule(
                    course_id=course.id,
                    start_time=now + timedelta(days=i),
                    end_time=now + timedelta(days=i, hours=1),
                    is_available=True,
                )
            )

    await db.commit()
    print("Schedules seeded!")