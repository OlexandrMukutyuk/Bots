from abc import ABC, abstractmethod


class AbstractDto(ABC):
    @abstractmethod
    def to_payload(self) -> dict:
        pass
