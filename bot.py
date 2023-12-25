import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

import data.config
import handlers.user


async def main():
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    bot = Bot(data.config.BOT_TOKEN, parse_mode="HTML")

    setup_aiogram(dp=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def setup_aiogram(dp: Dispatcher) -> None:
    setup_handlers(dp)
    setup_middlewares(dp)


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_routers(handlers.user.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    """For later"""


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
