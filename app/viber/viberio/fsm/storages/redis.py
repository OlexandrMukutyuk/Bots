import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, cast

from redis.asyncio.client import Redis

from viberio.fsm.states import State
from viberio.fsm.storages.base import StorageKey, BaseStorage, StateType, DEFAULT_DESTINY

DEFAULT_REDIS_LOCK_KWARGS = {"timeout": 60}
_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]


class KeyBuilder(ABC):
    """
    Base class for Redis key builder
    """

    @abstractmethod
    def build(self, key: StorageKey, part: str) -> str:
        """
        This method should be implemented in subclasses

        :param key: contextual key
        :param part: part of the record
        :return: key to be used in Redis queries
        """
        pass


class DefaultKeyBuilder(KeyBuilder):
    """
    Simple Redis key builder with default prefix.

    Generates a colon-joined string with prefix, chat_id, user_id,
    optional bot_id and optional destiny.
    """

    def __init__(
        self,
        *,
        prefix: str = "fsm",
        separator: str = ":",
        with_bot_id: bool = False,
        with_destiny: bool = False,
    ) -> None:
        """
        :param prefix: prefix for all records
        :param separator: separator
        :param with_bot_id: include Bot id in the key
        :param with_destiny: include destiny key
        """
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(self, key: StorageKey, part: str) -> str:
        parts = [self.prefix]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        if key.thread_id is not None:
            parts.append(str(key.thread_id))
        parts.append(str(key.user_id))
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Redis key builder is not configured to use key destiny other the default.\n"
                "\n"
                "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"
                "E.g: `RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))`"
            )
        parts.append(part)

        return self.separator.join(parts)


class RedisStorage(BaseStorage):
    """
    Redis storage required :code:`redis` package installed (:code:`pip install redis`)
    """

    def __init__(
        self,
        redis: Redis,
        key_builder: Optional[KeyBuilder] = None,
        state_ttl: Optional[Any] = None,
        data_ttl: Optional[Any] = None,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
    ) -> None:
        """
        :param redis: Instance of Redis connection
        :param key_builder: builder that helps to convert contextual key to string
        :param state_ttl: TTL for state records
        :param data_ttl: TTL for data records
        """
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.redis = redis
        self.key_builder = key_builder
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl
        self.json_loads = json_loads
        self.json_dumps = json_dumps

    async def close(self) -> None:
        await self.redis.close()

    async def set_state(
        self,
        key: StorageKey,
        state: StateType = None,
    ) -> None:
        redis_key = self.key_builder.build(key, "state")
        if state is None:
            await self.redis.delete(redis_key)
        else:
            await self.redis.set(
                redis_key,
                cast(str, state.state if isinstance(state, State) else state),
                ex=self.state_ttl,
            )

    async def get_state(
        self,
        key: StorageKey,
    ) -> Optional[str]:
        redis_key = self.key_builder.build(key, "state")
        value = await self.redis.get(redis_key)

        if isinstance(value, bytes):
            return value.decode("utf-8")
        return cast(Optional[str], value)

    async def set_data(
        self,
        key: StorageKey,
        data: Dict[str, Any],
    ) -> None:
        redis_key = self.key_builder.build(key, "data")
        if not data:
            await self.redis.delete(redis_key)
            return
        await self.redis.set(
            redis_key,
            self.json_dumps(data),
            ex=self.data_ttl,
        )

    async def get_data(
        self,
        key: StorageKey,
    ) -> Dict[str, Any]:
        redis_key = self.key_builder.build(key, "data")
        value = await self.redis.get(redis_key)
        if value is None:
            return {}
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return cast(Dict[str, Any], self.json_loads(value))
