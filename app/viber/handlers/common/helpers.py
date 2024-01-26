from typing import NamedTuple, Callable


class Handler(NamedTuple):
    handler: Callable
    filters: list


