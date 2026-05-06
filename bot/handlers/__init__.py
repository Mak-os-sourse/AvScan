from aiogram import Router
from bot.handlers.user_command import router as user_command
from bot.handlers.interval_parsing import router as interval_parsing_command
from bot.handlers.every_parsing import router as every_parsing_command
from bot.handlers.settings_task import router as settings_tasks_command
from bot.handlers.parsing import router as parsing_command
from bot.handlers.state import router as state_command

router = Router()
router.include_routers(
    user_command,
    interval_parsing_command,
    settings_tasks_command,
    every_parsing_command,
    parsing_command,
    state_command,
)