import asyncio
from aiogram import Dispatcher

from src.app.core.bot import bot
from src.app.core.cache import storage
from src.app.bot.middleware import setup_middlewares
from src.app.bot.handlers import router
from src.app.core.base import Base
from src.app.core.db import db
from src.app.core.tasks import start_parsing

async def main():
    await db.metadata_create_all(Base)
    
    dp = Dispatcher(storage=storage)
    
    dp.include_router(router)
    setup_middlewares(dp)
    
    await start_parsing.kiq()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())