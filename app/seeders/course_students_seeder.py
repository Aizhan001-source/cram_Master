from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data_access.db.models.course_student import CourseStudent
from data_access.db.models.course import Course
from data_access.db.models.student import Student


async def seed_course_students(db: AsyncSession):
    courses = (await db.execute(select(Course))).scalars().all()
    students = (await db.execute(select(Student))).scalars().all()

    if not courses or not students:
        print("No courses or students found!")
        return

    for i, student in enumerate(students):
        course = courses[i % len(courses)]

        result = await db.execute(
            select(CourseStudent).where(
                CourseStudent.course_id == course.id,
                CourseStudent.student_id == student.id
            )
        )
        exists = result.scalar_one_or_none()

        if not exists:
            db.add(
                CourseStudent(
                    course_id=course.id,
                    student_id=student.id
                )
            )

    await db.commit()
    print("CourseStudents seeded!")