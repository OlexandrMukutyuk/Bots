from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class VerifyAddressDto(AbstractDto):
    street_id: int
    house: str

    def to_payload(self) -> dict:
        return {"StreetId": self.street_id, "House": self.house}
