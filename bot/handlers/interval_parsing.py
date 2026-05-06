import time
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.fsm.user_fsm import IntervalParsing
from bot.keyboards.inline import back_main_menu
from bot.templates.messages import url_state, get_main_photo, get_interval_second
from services.queue import queue
from crud import TaskCRUD

router = Router()

@router.callback_query(F.data == "interval_parsing")
async def interval_parsing(callback: CallbackQuery, state: FSMContext):
    await state.set_state(IntervalParsing.url)
    return await callback.message.edit_caption(caption="Введите ссылку", reply_markup=back_main_menu())

@router.message(StateFilter(IntervalParsing.url))
async def get_url_interval(message: Message, state: FSMContext):
    if not await url_state(message, state, IntervalParsing):
        return
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption="Введите интервал от 120 мин",
        reply_markup=back_main_menu()
    )
    
@router.message(StateFilter(IntervalParsing.time))
async def get_interval(message: Message, state: FSMContext, session: AsyncSession):
    interval = await get_interval_second(message)
    if interval is None:
        return
    scheduled_at = int(time.time()) + interval
    url = (await state.get_data())["url"]
    task = await TaskCRUD.select(
        session, url=url,
        interval=interval,
        scheduled_at=scheduled_at,
        user_id=message.from_user.id,
        mode="Interval"
    )
    
    await queue.add_task(task)
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption="Интервальная таска созданна",
        reply_markup=back_main_menu()
    )