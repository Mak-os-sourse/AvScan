from aiogram import Dispatcher

from src.app.bot.middleware.db import DBMiddleware

from src.app.core.db import db

def setup_middlewares(dp: Dispatcher):
    dp.update.middleware(DBMiddleware(db.sessionmaker))