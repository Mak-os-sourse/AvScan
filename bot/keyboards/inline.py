from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.task import Tasks

def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔍 Разовый парсинг", callback_data="parsing"))
    builder.row(InlineKeyboardButton(text="✔ Интервальный парсинг", callback_data="interval_parsing"))
    builder.row(InlineKeyboardButton(text="💤 Ежедневный парсинг", callback_data="every_parsing"))
    builder.row(InlineKeyboardButton(text="⚙️ Настройка тасок", callback_data="settings_tasks"))
    builder.row(InlineKeyboardButton(text="📊 Моя статистика", callback_data="states"))
    return builder.as_markup()

def settings_tasks_menu(tasks: list[Tasks]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in tasks:
        builder.row(InlineKeyboardButton(text=f"Task url - {item.url}", callback_data=f"task_id:{item.id}"))
    builder.row(InlineKeyboardButton(text="В главное меню", callback_data="back_main_menu"))
    return builder.as_markup()

def task_manager_menu(task_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Удалить", callback_data=f"delete_task-id:{task_id}"))
    builder.row(InlineKeyboardButton(text="Изменить", callback_data=f"update_task-id:{task_id}"))
    builder.row(InlineKeyboardButton(text="Назад", callback_data=f"back_settings_tasks_menu"))

def back_settings_tasks_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Назад", callback_data=f"back_settings_tasks_menu"))
    return builder.as_markup()

def back_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="В главное меню", callback_data="back_main_menu"))
    return builder.as_markup()