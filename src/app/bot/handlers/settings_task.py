from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.bot.keyboards.inline import settings_tasks_menu, task_manager_menu, back_settings_tasks_menu
from src.app.crud.task import task_crud
from src.app.core.text import text

router = Router()

@router.callback_query(F.data == "settings_tasks")
async def get_tasks(callback: CallbackQuery, session: AsyncSession):
    tasks = await task_crud.get_all(session, user_id=callback.from_user.id)
    menu = settings_tasks_menu(tasks)
    await callback.message.edit_caption(caption=text.settings_tasks, reply_markup=menu)

@router.callback_query(F.data.startswith("task_id:"))
async def task_manager(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[-1])
    menu = task_manager_menu(task_id)
    await callback.message.edit_caption(caption=f"Task id - {task_id}", reply_markup=menu)

@router.callback_query(F.data.startswith("delete_task-id:"))
async def delete_task(callback: CallbackQuery, session: AsyncSession):
    task_id = int(callback.data.split(":")[-1])
    menu = back_settings_tasks_menu()
    await task_crud.delete(session, id=task_id)
    await callback.message.edit_caption(caption=f"Task id - {task_id} Удалена", reply_markup=menu)
