import asyncio
from aiogram.types import BufferedInputFile

from src.app.core.bot import bot
from src.app.core.text import text
from src.app.types.parser import Product
from src.app.core.broker_task import broker
from src.app.services.document import create_product_document

@broker.task
async def send_document(
    products: list[Product],
    user_id: int,
    wait: int = 0,
    ):
    await asyncio.sleep(wait)
    document = create_product_document(products)
    file = BufferedInputFile(document, filename="document.xlsx")
    await bot.send_document(user_id, document=file, caption=text.get_document)