from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RepairsDto(AbstractDto):
    user_id: str
    street_id: int

    def to_payload(self) -> dict:
        return {
            "UserId": self.user_id,
            "StreetId": self.street_id,
        }
