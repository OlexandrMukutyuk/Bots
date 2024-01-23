from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class SearchDto(AbstractDto):
    search: str

    def to_payload(self) -> dict:
        return {
            "Search": self.search,
        }
