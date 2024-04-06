import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode


BOT_TOKEN_ENV = "BOT_TOKEN"


async def main() -> None:
    BOT_TOKEN = os.getenv(BOT_TOKEN_ENV)
    if not BOT_TOKEN:
        raise ValueError(f"{BOT_TOKEN_ENV} is not set")

    logging.basicConfig(level=logging.INFO)

    dispatcher = Dispatcher()
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    await dispatcher.start_polling(bot)


asyncio.run(main())
