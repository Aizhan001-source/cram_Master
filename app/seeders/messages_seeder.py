from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from data_access.db.models.message import Message
from data_access.db.models.user import User


async def seed_messages(db: AsyncSession):
    users = (await db.execute(select(User))).scalars().all()

    if len(users) < 2:
        print("Not enough users for messages")
        return

    messages_data = [
        {
            "sender": users[0],
            "receiver": users[1],
            "content": "Hello! How are you?",
        },
        {
            "sender": users[1],
            "receiver": users[0],
            "content": "I'm good, thanks!",
        },
        {
            "sender": users[0],
            "receiver": users[1],
            "content": "Great to hear 👍",
        },
    ]

    for m in messages_data:
        db.add(
            Message(
                sender_id=m["sender"].id,
                receiver_id=m["receiver"].id,
                content=m["content"],
                is_read=False,
            )
        )

    await db.commit()
    print("Messages seeded!")