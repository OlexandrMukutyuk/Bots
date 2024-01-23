from typing import Optional, Type


class StatesGroup:
    pass


class State:
    def __init__(self, state: Optional[str] = None, group_name: Optional[str] = None) -> None:
        self._state = state
        self._group_name = group_name

    @property
    def state(self) -> Optional[str]:
        return f"{self._group_name}:{self._state}"

    def __set_name__(self, owner: Type[StatesGroup], name):
        if self._group_name is None:
            self._group_name = owner.__name__

        if self._state is None:
            self._state = name
