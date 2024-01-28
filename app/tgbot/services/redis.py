from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis

from data import config

redis_storage = RedisStorage(
    redis=Redis(
        host=config.FSM_HOST,
        password=config.FSM_PASSWORD,
        port=config.FSM_PORT,
        db=0,
    ),
    key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
)
