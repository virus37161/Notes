import logging
import sys
from aiogram import Bot, Dispatcher
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.middlewares.db import CounterMiddleware
from bot.handlers.handlers import router
from bot.handlers.send_notification import send_notification_term, send_notification_reminder
from bot.core.db import async_session
from bot.core.config import settings

TOKEN = settings.TOKEN
bot = Bot(TOKEN)

dp = Dispatcher()
dp.include_router(router)
router.message.middleware(CounterMiddleware(session_pool=async_session))

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler_reminder = AsyncIOScheduler(timezone="Europe/Moscow")

scheduler.add_job(send_notification_term, 'cron', hour='*', minute='*', args=[async_session, bot])
scheduler_reminder.add_job(send_notification_reminder, 'cron', hour='*', minute='*', args=[async_session, bot])


async def main() -> None:
    scheduler_reminder.start()
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
