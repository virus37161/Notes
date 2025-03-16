from sqlalchemy.future import select
from datetime import datetime
import asyncio
from bot.models.models import User, Note


async def send_notification_term(async_sessionmaker, bot):
    now = datetime.now()
    formatted_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    year, month, day = map(int, formatted_time_str[:10].split("-"))
    hour, minute, second = map(int, formatted_time_str[11:].split(":"))
    formatted_time_obj = datetime(year, month, day, hour, minute, second)

    async with async_sessionmaker() as session_obj:
        list_of_obj = await session_obj.execute(select(Note).filter(Note.term == formatted_time_obj))
        list_of_obj = list_of_obj.scalars().all()
        list_of_corutine = []
        if list_of_obj:
            for i in list_of_obj:
                list_of_corutine.append(send_message_of_term(i, session_obj, bot))
                i.overdue = True
                await session_obj.commit()
                await session_obj.refresh(i)
            result = await asyncio.gather(*list_of_corutine)


async def send_message_of_term(obj, session_obj, bot):
    id_chat = await get_id_chat(obj, session_obj)
    name_of_note = obj.name
    await bot.send_message(chat_id=id_chat, text=f"У вас сегодня срок '{name_of_note}'\n\
{obj.content[:30]}..."
                            )


async def get_id_chat(obj, session_obj):
    user = await session_obj.execute(select(User).where(User.id == obj.user_id))
    user = user.scalars().first()
    print(user.id)
    return user.id_chat


async def send_notification_reminder(async_sessionmaker, bot):
    now = datetime.now()
    formatted_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    year, month, day = map(int, formatted_time_str[:10].split("-"))
    hour, minute, second = map(int, formatted_time_str[11:].split(":"))
    formatted_time_obj = datetime(year, month, day, hour, minute, second)

    async with async_sessionmaker() as session_obj:
        list_of_obj = await session_obj.execute(select(Note).filter(Note.reminder == formatted_time_obj))
        list_of_obj = list_of_obj.scalars().all()

        list_of_corutine = []
        if list_of_obj:
            for i in list_of_obj:
                list_of_corutine.append(send_message_of_reminder(i, session_obj, bot))

            result = await asyncio.gather(*list_of_corutine)


async def send_message_of_reminder(obj, session_obj, bot):
    id_chat = await get_id_chat(obj, session_obj)
    name_of_note = obj.name
    await bot.send_message(chat_id=id_chat, text=f"У вас скоро срок '{name_of_note}'\n\
{obj.content[:30]}...\n\
Срок: {obj.term}"
                            )

