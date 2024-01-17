from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class GuestIdDto(AbstractDto):
    guest_id: str

    def to_payload(self) -> dict:
        return {
            "GuestId": self.guest_id,
        }
