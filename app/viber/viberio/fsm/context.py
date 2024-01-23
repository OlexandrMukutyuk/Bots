import copy
from typing import Optional, Dict, Any

from viberio.fsm.storages.base import BaseStorage, StorageKey, StateType


class FSMContext:
    def __init__(self, storage: BaseStorage, key: StorageKey) -> None:
        self.storage = storage
        self.key = key

    async def set_state(self, state: StateType = None) -> None:
        await self.storage.set_state(key=self.key, state=state)

    async def get_state(self) -> Optional[str]:
        return await self.storage.get_state(key=self.key)

    async def set_data(self, data: Dict[str, Any]) -> None:
        await self.storage.set_data(key=self.key, data=data)

    async def get_data(self) -> Dict[str, Any]:
        return await self.storage.get_data(key=self.key)

    async def update_data(
            self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        if data:
            kwargs.update(data)
        return await self.storage.update_data(key=self.key, data=kwargs)

    async def reset_state(self) -> None:
        await self.set_state(state=None)

    async def reset_data(self) -> None:
        await self.set_data({})

    async def clear(self) -> None:
        await self.set_state(state=None)
        await self.set_data({})


class FSMContextProxy:
    def __init__(self, fsm_context: FSMContext):
        super(FSMContextProxy, self).__init__()
        self.fsm_context = fsm_context
        self._copy = {}
        self._data = {}
        self._state = None
        self._is_dirty = False

        self._closed = True

    async def __aenter__(self):
        await self.load()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.save()
        self._closed = True

    def _check_closed(self):
        if self._closed:
            raise LookupError('Proxy is closed!')

    @classmethod
    async def create(cls, fsm_context: FSMContext):
        """
        :param fsm_context:
        :return:
        """
        proxy = cls(fsm_context)
        await proxy.load()
        return proxy

    async def load(self):
        self._closed = False

        self.clear()
        self._state = await self.fsm_context.get_state()
        self.update(await self.fsm_context.get_data())
        self._copy = copy.deepcopy(self._data)
        self._is_dirty = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._check_closed()

        self._state = value
        self._is_dirty = True

    @state.deleter
    def state(self):
        self._check_closed()

        self._state = None
        self._is_dirty = True

    async def save(self, force=False):
        self._check_closed()

        if self._copy != self._data or force:
            await self.fsm_context.set_data(data=self._data)
        if self._is_dirty or force:
            await self.fsm_context.set_state(self.state)
        self._is_dirty = False
        self._copy = copy.deepcopy(self._data)

    def clear(self):
        del self.state
        return self._data.clear()

    def get(self, value, default=None):
        return self._data.get(value, default)

    def setdefault(self, key, default):
        self._check_closed()

        return self._data.setdefault(key, default)

    def update(self, data=None, **kwargs):
        self._check_closed()

        if data is None:
            data = {}
        self._data.update(data, **kwargs)

    def pop(self, key, default=None):
        self._check_closed()

        return self._data.pop(key, default)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def as_dict(self):
        return copy.deepcopy(self._data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._check_closed()

        self._data[key] = value

    def __delitem__(self, key):
        self._check_closed()

        del self._data[key]

    def __contains__(self, item):
        return item in self._data

    def __str__(self):
        readable_state = f"'{self.state}'" if self.state else "<default>"
        result = f"{self.__class__.__name__} state = {readable_state}, data = {self._data}"
        if self._closed:
            result += ', closed = True'
        return result
