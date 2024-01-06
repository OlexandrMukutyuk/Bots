import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from redis.asyncio import Redis

from app.tgbot.data import config
from app.tgbot.data.config import (
    BOT_TOKEN,
    WEBHOOK_ADDRESS,
    WEBHOOK_PATH,
    WEBHOOK_LISTENING_HOST,
    WEBHOOK_LISTENING_PORT,
    WEBHOOK_SECRET_TOKEN,
)
from app.tgbot.handlers import auth, cabinet
from app.tgbot.web_handlers.media import media


def setup_web_handlers(app: web.Application) -> None:
    app.router.add_route(method="GET", path="/media/{file_name}", handler=media)


def setup_handlers(dp: Dispatcher) -> None:
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


def main() -> None:
    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=config.FSM_HOST,
                password=config.FSM_PASSWORD,
                port=config.FSM_PORT,
                db=0,
            ),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    )

    setup_aiogram(dp)

    dp.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

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
    web.run_app(app, host=WEBHOOK_LISTENING_HOST, port=WEBHOOK_LISTENING_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
