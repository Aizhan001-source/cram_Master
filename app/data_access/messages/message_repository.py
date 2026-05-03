from sqlalchemy import select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from data_access.db.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, sender_id: UUID, receiver_id: UUID, content: str):
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    # 🔥 СООБЩЕНИЯ ДИАЛОГА
    async def get_conversation(self, user1_id: UUID, user2_id: UUID):
        result = await self.db.execute(
            select(Message)
            .where(
                or_(
                    and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                    and_(Message.sender_id == user2_id, Message.receiver_id == user1_id),
                )
            )
            .options(
                selectinload(Message.sender),
                selectinload(Message.receiver)
            )
            .order_by(Message.created_at)
        )
        return result.scalars().all()

    # 🔥 ЧАТЫ (ПОСЛЕДНЕЕ СООБЩЕНИЕ НА ДИАЛОГ)
    async def get_my_chats(self, user_id: UUID):
        result = await self.db.execute(
            select(Message)
            .where(or_(Message.sender_id == user_id, Message.receiver_id == user_id))
            .options(
                selectinload(Message.sender),
                selectinload(Message.receiver)
            )
            .order_by(Message.created_at.desc())
        )

        messages = result.scalars().all()

        seen = set()
        chats = []

        for msg in messages:
            other_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id

            if other_id not in seen:
                seen.add(other_id)
                chats.append(msg)

        return chats

    async def mark_as_read(self, sender_id: UUID, receiver_id: UUID):
        result = await self.db.execute(
            select(Message).where(
                Message.sender_id == sender_id,
                Message.receiver_id == receiver_id,
                Message.is_read == False
            )
        )

        for msg in result.scalars().all():
            msg.is_read = True

        await self.db.commit()

    async def get_unread_count(self, receiver_id: UUID):
        result = await self.db.execute(
            select(Message).where(
                Message.receiver_id == receiver_id,
                Message.is_read == False
            )
        )
        return len(result.scalars().all())