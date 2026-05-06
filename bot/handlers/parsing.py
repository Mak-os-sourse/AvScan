from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.templates.messages import check_url
from bot.keyboards.inline import back_main_menu
from bot.fsm.user_fsm import Parsing
from services.queue import queue

router = Router()

@router.callback_query(F.data == "parsing")
async def parisng(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Parsing.url)
    menu = back_main_menu()
    return callback.message.edit_caption(caption="Введите ссылку", reply_markup=menu)

@router.message(StateFilter(Parsing.url))
async def get_url(message: Message, state: FSMContext):
    if not await check_url(message):
        return
    await state.update_data(url=message.text)
    uuid = await queue.add_fast_parse()
    
    photo = FSInputFile("static/main.png")
    return await message.answer_photo(
        photo=photo,
        caption="Разовая таска созданна",
        reply_markup=back_main_menu()
    )