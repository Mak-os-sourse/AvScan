from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from src.app.bot.fsm.user_fsm import Start
from src.app.bot.templates.messages import main_menu_msg
from src.app.crud.user import user_crud

router = Router()

@router.message(CommandStart())
async def start(message: Message, session: AsyncSession, state: FSMContext):
    user_id = message.from_user.id
    user = await user_crud.get(session, id=user_id)
    if user is None:
        user = await user_crud.create(session, id=user_id, username=message.from_user.username)
        
    await state.update_data(user={
        "id": user.id,
        "username": user.username,
    })
    await state.set_state(Start.user)
    return await main_menu_msg(message, first_name=message.from_user.first_name)
    
@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    user = await user_crud.get(session, id=callback.from_user.id)
    await state.update_data(user={
        "id": user.id,
        "username": user.username,
    })
    await state.set_state(Start.user)
    return await main_menu_msg(
        callback.message,
        first_name=callback.from_user.first_name,
        edit=True
    )