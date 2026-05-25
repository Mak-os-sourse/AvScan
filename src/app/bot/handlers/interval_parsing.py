import time
from aiogram import Router, F
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.app.bot.fsm.user_fsm import IntervalParsing, Start
from src.app.bot.keyboards.inline import back_main_menu
from src.app.bot.templates.messages import check_url, get_main_photo, get_interval_second
from src.app.services.queue import queue
from src.app.crud.task import task_crud
from src.app.core.text import text

router = Router()

@router.callback_query(F.data == "interval_parsing", StateFilter(Start.user))
async def interval_parsing(callback: CallbackQuery, state: FSMContext):
    user = await state.get_value("user")
    await state.set_state(IntervalParsing.url)
    await state.update_data(user=user)
    return await callback.message.edit_caption(caption=text.input_url, reply_markup=back_main_menu())

@router.message(StateFilter(IntervalParsing.url))
async def get_url(message: Message, state: FSMContext):
    if not await check_url(message):
        return
    await state.update_data(url=message.text)
    await state.set_state(IntervalParsing.time)
    
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption=text.input_interval,
        reply_markup=back_main_menu()
    )
    
@router.message(StateFilter(IntervalParsing.time))
async def get_interval(message: Message, state: FSMContext, session: AsyncSession, redis: Redis):
    user = await state.get_value("user")
    interval = await get_interval_second(message)
    if interval is None:
        return
    scheduled_at = int(time.time()) + interval
    url = await state.get_value("url")
    task = await task_crud.create(
        session, url=url,
        interval=interval,
        scheduled_at=scheduled_at,
        user_id=user["id"],
    )
    
    await queue.add_task(redis, task)
    photo = get_main_photo()
    return await message.answer_photo(
        photo=photo,
        caption=text.create_task,
        reply_markup=back_main_menu()
    )