from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.task import task_crud
from src.app.bot.templates.messages import menu_state

router = Router()

@router.callback_query(F.data == "states")
async def get_state(callback: CallbackQuery, session: AsyncSession):
    tasks = await task_crud.get_all(session, user_id=callback.from_user.id)
    len_list = len(tasks)
    count_running = 0
    for item in tasks:
        count_running += item.launches 
    return await menu_state(callback.message, count_running=count_running, len_list=len_list)