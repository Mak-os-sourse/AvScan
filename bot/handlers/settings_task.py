from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.fsm.user_fsm import IntervalParsing, EverylParsing
from bot.keyboards.inline import settings_tasks_menu, task_manager_menu, back_settings_tasks_menu
from crud import TaskCRUD

router = Router()

@router.callback_query(F.data == "settings_tasks", F.data.startswith("back_settings_tasks_menu"))
async def get_tasks(callback: CallbackQuery, session: AsyncSession):
    tasks = await TaskCRUD.get(session, user_id=callback.from_user.id)
    if not tasks:
        pass
    menu = settings_tasks_menu(tasks)
    await callback.message.edit_caption(caption="Все ваши таски", reply_markup=menu)
    
@router.callback_query(F.data.startswith("task_id:"))
async def task_manager(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[-1])
    menu = task_manager_menu(task_id)
    await callback.message.edit_caption(caption=f"Task id - {task_id}", reply_markup=menu)

@router.callback_query(F.data.startswith("delete_task-id:"))
async def delete_task(callback: CallbackQuery, session: AsyncSession):
    task_id = int(callback.data.split(":")[-1])
    menu = back_settings_tasks_menu()
    await TaskCRUD.delete(session, id=task_id)
    await callback.message.edit_caption(caption=f"Task id - {task_id} Удалена", reply_markup=menu)
    
@router.callback_query(F.data.startswith("update_task-id:"))
async def delete_task(callback: CallbackQuery, session: AsyncSession):
    task_id = int(callback.data.split(":")[-1])
    menu = back_settings_tasks_menu()
    await callback.message.edit_caption(caption=f"Task id - {task_id} Удалена", reply_markup=menu)