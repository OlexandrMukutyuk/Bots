from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class ChooseRegionDto(AbstractDto):
    user_id: int
    region: str

    def to_payload(self) -> dict:
        return {"UserId": self.user_id, "Region": self.region}
