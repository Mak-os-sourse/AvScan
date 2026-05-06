from aiogram import Dispatcher

from bot.middleware.db import DBMiddleware

from core.db import db

def setup_middlewares(dp: Dispatcher):
    dp.update.middleware(DBMiddleware(db.sessionmaker))