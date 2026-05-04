from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from data_access.db.models.schedule import Schedule
from data_access.db.models.tutor import Tutor


async def seed_schedules(db: AsyncSession):

    tutors = (await db.execute(select(Tutor))).scalars().all()

    if not tutors:
        print("❌ No tutors found")
        return

    created = 0

    start_dt = datetime(2026, 1, 1, 10, 0, 0)
    end_dt = datetime(2026, 1, 1, 11, 0, 0)

    for tutor in tutors:

        exists = (await db.execute(
            select(Schedule).where(
                Schedule.course_id == tutor.id,
                Schedule.start_time == start_dt
            )
        )).scalar_one_or_none()

        if exists:
            continue

        db.add(Schedule(
            course_id=tutor.id,
            start_time=start_dt,
            end_time=end_dt,
            is_available=True
        ))

        created += 1

    await db.commit()
    print(f"✅ schedules seeded: {created}")