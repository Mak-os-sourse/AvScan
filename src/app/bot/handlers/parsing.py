from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.app.bot.templates.messages import check_url, get_main_photo
from src.app.bot.keyboards.inline import back_main_menu
from src.app.bot.fsm.user_fsm import Parsing, Start
from src.app.services.queue import queue
from src.app.core.text import text

router = Router()

@router.callback_query(F.data == "parsing", StateFilter(Start.user))
async def parisng(callback: CallbackQuery, state: FSMContext):
    user = await state.get_value("user")
    await state.set_state(Parsing.url)
    await state.update_data(user=user)
    menu = back_main_menu()
    return await callback.message.edit_caption(caption=text.input_url, reply_markup=menu)

@router.message(StateFilter(Parsing.url))
async def get_url(message: Message, state: FSMContext):
    if not await check_url(message):
        return
    url = message.text
    user = await state.get_value("user")
    
    await state.update_data(url=url)
    await queue.add_fast_task(url=url, user_id=user["id"])
    
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption=text.create_task,
        reply_markup=back_main_menu()
    )