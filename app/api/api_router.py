from fastapi import APIRouter

from api.users.user_api import router as users_router
from api.tutors.tutor_api import router as tutor_router
from api.messages.message_api import router as message_router
from api.students.student_api import router as student_router
from api.payments.payment_api import router as payment_router
from api.bookings.booking_api import router as booking_router
from api.reviews.review_api import router as review_router
from api.courses.course_api import router as course_router
from api.subjects.subject_api import router as subject_router
from api.roles.role_api import router as role_api
from api.schedules.schedule_api import router as schedule_router
from api.favorites.favorite_api import router as favorite_router
from api.educations.education_api import router as education_router


api_router = APIRouter()

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["USER"]
)

api_router.include_router(
    tutor_router,
    prefix="/tutors",
    tags=["TUTOR"]
)

api_router.include_router(
    message_router,
    prefix="/messages",
    tags=["MESSAGE"]
)

api_router.include_router(
    student_router,
    prefix="/students",
    tags=["STUDENT"]
)

api_router.include_router(
    payment_router,
    prefix="/payments",
    tags=["PAYMENT"]
)

api_router.include_router(
    booking_router,
    prefix="/bookings",
    tags=["BOOKING"]
)

api_router.include_router(
    review_router,
    prefix="/reviews",
    tags=["REVIEW"]
)

api_router.include_router(
    course_router,
    prefix="/courses",
    tags=["COURSE"]
)

api_router.include_router(
    subject_router,
    prefix="/subjects",
    tags=["SUBJECTS"]
)

api_router.include_router(
    role_api,
    prefix="/roles",
    tags=["ROLES"]
)

api_router.include_router(
    schedule_router,
    prefix="/schedule",
    tags=["SCHEDULE"]
)

api_router.include_router(
    favorite_router, 
    prefix="/favorites",
    tags=["FAVORITES"]
)

api_router.include_router(
    education_router, 
    prefix="/educations",
     tags=["EDUCATIONS"]
)
