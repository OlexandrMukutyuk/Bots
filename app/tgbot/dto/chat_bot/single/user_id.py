from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class UserIdDto(AbstractDto):
    user_id: int

    def to_payload(self) -> dict:
        return {"UserId": self.user_id}
