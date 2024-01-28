from redis.asyncio import Redis

from data import config
from viberio.fsm.storages.redis import RedisStorage, DefaultKeyBuilder

redis_storage = RedisStorage(
    redis=Redis(host=config.FSM_HOST, port=config.FSM_PORT, db=1, password=config.FSM_PASSWORD),
    key_builder=DefaultKeyBuilder(
        prefix="fsm",
        separator=":",
        with_bot_id=True,
    ),
)
