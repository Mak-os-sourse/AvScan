from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from bot.templates.messages import main_menu_msg
from crud import UserCRUD

router = Router()

@router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    await UserCRUD.select_not_exist(
        session,
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    return await main_menu_msg(message, first_name=message.from_user.first_name)
    
@router.callback_query(F.data == "back_main_menu")
async def back_main_menu(callback: CallbackQuery):
    return await main_menu_msg(
        callback.message,
        first_name=callback.from_user.first_name,
        edit=True
    )