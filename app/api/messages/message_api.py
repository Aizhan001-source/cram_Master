from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api.messages.message_router import router
from api.messages.message_schemas import MessageCreate, MessageRead, ChatPreview, UnreadCountResponse

from business_logic.messages.message_service import MessageService
from data_access.messages.message_repository import MessageRepository
from data_access.db.session import get_db
from utils.auth_middleware import get_current_user


def get_message_service(db: AsyncSession = Depends(get_db)) -> MessageService:
    return MessageService(MessageRepository(db))


@router.get("/chats", response_model=list[ChatPreview])
async def get_chats(
    service: MessageService = Depends(get_message_service),
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"]))
):
    return await service.get_my_chats(current_user.id)


@router.get("/unread", response_model=UnreadCountResponse)
async def unread(
    service: MessageService = Depends(get_message_service),
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"])),
):
    return await service.get_unread_count(current_user.id)


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(
    data: MessageCreate,
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"])),
    service: MessageService = Depends(get_message_service),
):
    return await service.send_message(current_user.id, data)


@router.get("/{other_user_id}", response_model=list[MessageRead])
async def conversation(
    other_user_id: UUID,
    current_user=Depends(get_current_user(required_roles=["student", "admin", "tutor"])),
    service: MessageService = Depends(get_message_service),
):
    return await service.get_conversation(
        current_user.id,
        other_user_id,
    )