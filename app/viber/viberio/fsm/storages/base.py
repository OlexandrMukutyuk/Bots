from abc import ABC, abstractmethod
from typing import Union, Optional, Dict, Any

from attr import dataclass

from viberio.fsm.states import State

DEFAULT_DESTINY = "default"

StateType = Optional[Union[str, State]]


@dataclass(frozen=True)
class StorageKey:
    bot_id: str
    user_id: str
    thread_id: Optional[int] = None
    destiny: str = DEFAULT_DESTINY


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


class BaseStorage(ABC):
    """
    Base class for all FSM storages
    """

    @abstractmethod
    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        pass

    @abstractmethod
    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        pass

    @abstractmethod
    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        pass

    @abstractmethod
    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        pass

    async def update_data(self, key: StorageKey, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Update date in the storage for key (like dict.update())

        :param key: storage key
        :param data: partial data
        :return: new data
        """
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data.copy()

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Close storage (database connection, file or etc.)
        """
        pass
