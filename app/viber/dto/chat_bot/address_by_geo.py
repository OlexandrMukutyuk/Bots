from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class AddressByGeoDto(AbstractDto):
    user_id: int
    lat: float
    lng: float

    def to_payload(self) -> dict:
        return {"UserId": self.user_id, "Lat": self.lat, "Lng": self.lng}
