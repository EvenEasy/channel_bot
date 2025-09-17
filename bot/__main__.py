import sys

import asyncio
import logging

import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from bot.core.config import Config
from bot.core.database import DataBase
from bot.core.scheduler import Scheduler
from bot.routers import setup_routers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(Config.token(), default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True))
    dp = Dispatcher()
    db = DataBase()
    scheduler = Scheduler(bot.token, sqlite_path='sqlite:///jobs.db', parse_mode='HTML')
    await db.sync()

    await bot.delete_webhook()

    setup_routers(dp)

    scheduler.start()

    await dp.start_polling(
        bot,
        _db=db,
        _scheduler=scheduler,
        allowed_updates=dp.resolve_used_update_types()
    )

asyncio.run(main())
