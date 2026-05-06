import asyncio
from aiogram import Dispatcher, Bot

from core.cache import storage
from bot.middleware import setup_middlewares
from core.settings import settings
from bot.handlers import router
from core.base import Base
from core.db import db

async def main():
    await db.metadata_create_all(Base)
    
    bot = Bot(settings.TOKEN)
    dp = Dispatcher(storage=storage)
    
    dp.include_router(router)
    setup_middlewares(dp)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())