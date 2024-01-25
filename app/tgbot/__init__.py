import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot import bot, redis_storage
from data.config import (
    WEBHOOK_ADDRESS,
    WEBHOOK_PATH,
    WEBHOOK_LISTENING_HOST,
    WEBHOOK_LISTENING_PORT,
    WEBHOOK_SECRET_TOKEN,
)
from handlers import start, guest, advanced
from web_handlers.media import media
from web_handlers.push_notification import push_notification


def setup_web_handlers(app: web.Application) -> None:
    app.router.add_route(method="GET", path="/media/{file_name}", handler=media)
    app.router.add_route(method="POST", path="/push-notification", handler=push_notification)


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.prepare_router())
    dp.include_router(guest.prepare_router())
    dp.include_router(advanced.prepare_router())


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
