import asyncio
import logging
import sys

from aiohttp import web
from redis.asyncio import Redis

from viberio.api.client import ViberBot
from viberio.dispatcher.dispatcher import Dispatcher
from viberio.dispatcher.filters.builtin import StateFilter
from viberio.dispatcher.webhook import ViberWebhookView
from viberio.fsm.states import StatesGroup, State
from viberio.fsm.storages.redis import RedisStorage, DefaultKeyBuilder
from viberio.types import messages, requests
from viberio.types.configuration import BotConfiguration
from viberio.types.messages.keyboard_message import Keyboard, ButtonsObj

API_TOKEN = '52476a0599a7df5b-67dd9d37831c2c3a-2acb584506924f2b'
WEBHOOK_URL = 'https://285d-193-239-235-240.ngrok-free.app'

loop = asyncio.get_event_loop()

app = web.Application()
bot_config = BotConfiguration(auth_token=API_TOKEN, name='Test bot')
viber = ViberBot(bot_config)

redis_storage = RedisStorage(
    redis=Redis(
        host='localhost',
        port=6379,
        db=1,
        password='password'
    ),
    key_builder=DefaultKeyBuilder(
        prefix="fsm",
        separator=":",
        with_bot_id=True,
    )
)

dp = Dispatcher(viber, redis_storage)

ViberWebhookView.bind(dp, app, '/')


@dp.text_messages_handler()
async def start(request: requests.ViberMessageRequest, data: dict):
    text = messages.TextMessage(text=request.message.text)

    dp_ = Dispatcher.get_current()
    state = dp_.current_state(request)

    return await viber.send_message(request.sender.id, text)




async def set_webhook():
    await asyncio.sleep(1)
    await viber.set_webhook(WEBHOOK_URL)


async def on_shutdown(application: web.Application):
    await viber.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.on_shutdown.append(on_shutdown)
    loop.create_task(set_webhook())
    web.run_app(app, host='0.0.0.0', port=8080, loop=loop)
