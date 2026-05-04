from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.users.user_schemas import UserAdminCreate, UserCreate, UserLogin, UserRead
from utils.auth_middleware import get_current_user
from business_logic.users.user_service import UserService
from business_logic.email_service import send_email
from core.security import create_reset_token, decode_reset_token
from data_access.db.session import get_db
from data_access.db.models.user import User
from sqlalchemy import select

router = APIRouter()
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserRead)
async def user_register(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(user.first_name, user.last_name, user.email, user.password, user.role_id)


@router.post("/login")
async def user_login(
    user: UserLogin,
    service: UserService = Depends(get_user_service),
):
    result = await service.login_user(user.email, user.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result

@router.get("/all")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user(required_roles=["admin"])),
):
    result = await service.get_all_users()
    
    return result


@router.get("/profile")
async def get_user_profile(
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user(required_roles=["student", "tutor"])),

):
    result = await service.get_user_profile(user.get("user_id"))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result

@router.post("/forgot-password")
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        return {"message": "If email exists, link sent"}

    token = create_reset_token({"sub": str(user.id)})

    link = f"http://localhost:3000/reset-password?token={token}"

    send_email(email, link)

    return {"message": "Check your email"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: AsyncSession = Depends(get_db)
):
    payload = decode_reset_token(token)
    user_id = payload.get("user_id")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()

    user.password = new_password  # ❗ лучше захешировать
    await db.commit()

    return {"message": "Password updated"}