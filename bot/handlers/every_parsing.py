import re
from datetime import datetime
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.templates.messages import url_state, get_main_photo, get_interval_second
from bot.fsm.user_fsm import EverylParsing
from bot.keyboards.inline import back_main_menu
from services.queue import queue
from crud import TaskCRUD
 
router = Router()

@router.callback_query(F.data == "every_parsing")
async def interval_parsing(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EverylParsing.url)
    return callback.message.edit_caption(caption="Введите ссылку", reply_markup=back_main_menu())

@router.message(StateFilter(EverylParsing.url))
async def get_url_interval(message: Message, state: FSMContext):
    if not await url_state(message, state):
        return
    await state.set_state(EverylParsing.interval)
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption="Введите время когда отдать отчет",
        reply_markup=back_main_menu()
    )
    
@router.message(StateFilter(EverylParsing.time))
async def get_interval(message: Message, state: FSMContext, session: AsyncSession):
    text = message.text
    if re.search(r"\d+/\d+", text) is None:
        return await message.answer("Интервал не правильный, должен быть часы/минуты")
    now = datetime.now()
    scheduled_at = datetime.strptime(text, "%H/%M").replace(
        year=now.year,
        month=now.month,
        day=now.day + 1
    ).timestamp()
    scheduled_at = int(scheduled_at)
    url = (await state.get_data())["url"]
    task = await TaskCRUD.select(
        session, url=url,
        scheduled_at=scheduled_at,
        user_id=message.from_user.id,
        mode="Every"
    )
    
    await queue.add_task(task)
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption="Ежедневная таска созданна",
        reply_markup=back_main_menu()
    )