from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.message import Message
from data_access.db.models.user import User


async def seed_messages(db: AsyncSession):
    users = (await db.execute(select(User))).scalars().all()

    if len(users) < 2:
        print("Not enough users for messages")
        return

    exists = await db.execute(select(Message).limit(1))
    if exists.scalar_one_or_none():
        print("Messages already seeded")
        return

    messages = [
        Message(sender_id=users[0].id, receiver_id=users[1].id, content="Hello! How are you?", is_read=False),
        Message(sender_id=users[1].id, receiver_id=users[0].id, content="I'm good, thanks!", is_read=False),
        Message(sender_id=users[0].id, receiver_id=users[1].id, content="Great to hear 👍", is_read=False),
    ]

    db.add_all(messages)
    await db.commit()

    print("Messages seeded!")