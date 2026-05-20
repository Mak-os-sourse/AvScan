import re
from aiogram.types import Message, FSInputFile

from src.app.bot.keyboards.inline import main_menu
from src.app.bot.keyboards.inline import back_main_menu

def get_main_photo() -> FSInputFile:
    return FSInputFile("static/3.jpg")

async def main_menu_msg(message: Message, first_name: str, edit: bool = False):
    menu = main_menu()
    if edit:
        return await message.edit_caption(
            caption=f"Привет, {first_name}!",
            reply_markup=menu
        )
    else:
        photo = get_main_photo()
        return await message.answer_photo(
            photo=photo, caption=f"Привет, {first_name}!",
            reply_markup=menu
        )

async def get_interval_second(message: Message) -> int | None:
    text = message.text
    if not text.isdigit():
        await message.answer("Интервал не правильный, должен быть в минутах")
        return
    interval = int(text)
    if interval <= 120:
        await message.answer("Интервал должен быть от 120 мин")
        return
    return interval * 60


async def menu_state(message: Message, count_running: int, len_list: int):
    menu = back_main_menu()
    await message.edit_caption(
        caption=f"Запусков {count_running}\nКоличество тасок {len_list}",
        reply_markup=menu
    )

async def check_url(message: Message) -> bool:
    find_url = re.search(r"^https://www.avito.ru/\w+", message.text)
    if find_url is None:
        await message.answer("Ссылка не правильная")
        return False
    return True