from aiogram import Router
from src.app.bot.handlers.user_command import router as user_command
from src.app.bot.handlers.interval_parsing import router as interval_parsing_command
from src.app.bot.handlers.settings_task import router as settings_tasks_command
from src.app.bot.handlers.parsing import router as parsing_command
from src.app.bot.handlers.state import router as state_command

router = Router()
router.include_routers(
    user_command,
    interval_parsing_command,
    settings_tasks_command,
    parsing_command,
    state_command,
)