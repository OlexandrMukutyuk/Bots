import asyncio
import logging
import sys

from aiohttp import web
from redis.asyncio import Redis

from data import config
from handlers import guest, start, advanced
from viber import viber
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.webhook import ViberWebhookView
from viberio.fsm.storages.redis import RedisStorage, DefaultKeyBuilder

loop = asyncio.get_event_loop()

app = web.Application()

redis_storage = RedisStorage(
    redis=Redis(host=config.FSM_HOST, port=config.FSM_PORT, db=1, password=config.FSM_PASSWORD),
    key_builder=DefaultKeyBuilder(
        prefix="fsm",
        separator=":",
        with_bot_id=True,
    ),
)

dispatcher = Dispatcher(viber, redis_storage)
ViberWebhookView.bind(dispatcher, app, "/")


async def set_webhook():
    await asyncio.sleep(1)
    await viber.set_webhook(config.WEBHOOK_ADDRESS)


async def on_shutdown(application: web.Application):
    await viber.close()


def register_handlers(dp: Dispatcher):
    start.prepare_router(dp)
    guest.prepare_router(dp)
    advanced.prepare_router(dp)


if __name__ == "__main__":
    register_handlers(dispatcher)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.on_shutdown.append(on_shutdown)
    loop.create_task(set_webhook())
    web.run_app(
        app, host=config.WEBHOOK_LISTENING_HOST, port=config.WEBHOOK_LISTENING_PORT, loop=loop
    )
