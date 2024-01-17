import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from redis.asyncio import Redis

from data import config
from data.config import (
    BOT_TOKEN,
    WEBHOOK_ADDRESS,
    WEBHOOK_PATH,
    WEBHOOK_LISTENING_HOST,
    WEBHOOK_LISTENING_PORT,
    WEBHOOK_SECRET_TOKEN,
)
from handlers import auth, cabinet, start, subscription
from web_handlers.media import media

# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)


def setup_web_handlers(app: web.Application) -> None:
    app.router.add_route(method="GET", path="/media/{file_name}", handler=media)


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.prepare_router())
    dp.include_router(subscription.prepare_router())
    dp.include_router(auth.prepare_router())
    dp.include_router(cabinet.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    pass


def setup_aiogram(dp: Dispatcher) -> None:
    print("Configuring aiogram")
    setup_handlers(dp)
    setup_middlewares(dp)
    print("Configured aiogram")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{WEBHOOK_ADDRESS}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET_TOKEN,
    )


async def delete_updates(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)


def main() -> None:
    loop = asyncio.new_event_loop()

    redis_storage = RedisStorage(
        redis=Redis(
            host=config.FSM_HOST,
            password=config.FSM_PASSWORD,
            port=config.FSM_PORT,
            db=0,
        ),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )

    mem_storage = MemoryStorage()

    dp = Dispatcher(storage=redis_storage)

    setup_aiogram(dp)

    dp.startup.register(on_startup)

    loop.run_until_complete(delete_updates(bot))

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET_TOKEN,
    )

    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    setup_web_handlers(app)

    # And finally start webserver
    web.run_app(app, host=WEBHOOK_LISTENING_HOST, port=WEBHOOK_LISTENING_PORT, loop=loop)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
