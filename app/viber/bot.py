import asyncio
import logging
import sys

from aiohttp import web

from data import config
from handlers import guest, start, advanced
from services.database import DB
from services.redis import redis_storage
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.webhook import ViberWebhookView
from web_handlers.media import media
from web_handlers.push_notification import push_notification

loop = asyncio.get_event_loop()

app = web.Application()


dispatcher = Dispatcher(viber, redis_storage)
ViberWebhookView.bind(dispatcher, app, config.WEBHOOK_PATH)


async def set_webhook():
    await asyncio.sleep(1)
    await viber.set_webhook(config.WEBHOOK_ADDRESS)


async def on_shutdown(application: web.Application):
    await viber.close()


def setup_webhandlers(app: web.Application):
    app.router.add_route(method="GET", path="/media/{file_name}", handler=media)
    app.router.add_route(method="POST", path="/push-notification", handler=push_notification)


def register_handlers(dp: Dispatcher):
    start.prepare_router(dp)
    guest.prepare_router(dp)
    advanced.prepare_router(dp)


if __name__ == "__main__":
    loop.create_task(DB.setup_database())
    register_handlers(dispatcher)
    setup_webhandlers(app)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.on_shutdown.append(on_shutdown)
    loop.create_task(set_webhook())
    web.run_app(
        app, host=config.WEBHOOK_LISTENING_HOST, port=config.WEBHOOK_LISTENING_PORT, loop=loop
    )
