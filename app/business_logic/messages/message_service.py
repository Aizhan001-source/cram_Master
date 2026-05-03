from uuid import UUID
from fastapi import HTTPException
from data_access.messages.message_repository import MessageRepository
from api.messages.message_schemas import MessageCreate


class MessageService:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    async def send_message(self, sender_id: UUID, data: MessageCreate):
        if sender_id == data.receiver_id:
            raise HTTPException(400, "Нельзя отправить сообщение самому себе")

        return await self.repo.create_message(
            sender_id=sender_id,
            receiver_id=data.receiver_id,
            content=data.content,
        )

    async def get_conversation(self, user_id: UUID, other_user_id: UUID):
        await self.repo.mark_as_read(other_user_id, user_id)

        return await self.repo.get_conversation(user_id, other_user_id)

    async def get_my_chats(self, user_id: UUID):
        return await self.repo.get_my_chats(user_id)

    async def get_unread_count(self, user_id: UUID):
        return {"unread_count": await self.repo.get_unread_count(user_id)}