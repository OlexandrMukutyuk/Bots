from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RepairsGuestDto(AbstractDto):
    guest_id: str
    street_id: int
    house: str

    def to_payload(self) -> dict:
        return {
            "GuestId": self.guest_id,
            "StreetId": self.street_id,
            "House": self.house,
        }
