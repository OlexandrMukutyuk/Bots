# Initialize Bot instance with a default parse mode which will be passed to all API calls
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis, ConnectionPool

from data import config
from data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

redis_pool = Redis(
    connection_pool=ConnectionPool(
        host=config.FSM_HOST,
        port=config.FSM_PORT,
        password=config.FSM_PASSWORD,
        db=0,
    )
)

redis_storage = RedisStorage(
    redis=Redis(
        host=config.FSM_HOST,
        password=config.FSM_PASSWORD,
        port=config.FSM_PORT,
        db=0,
    ),
    key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
)
