from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class CreateRequestDto(AbstractDto):
    user_id: int
    problem_id: int
    reason_id: int
    city_id: int
    street_id: int
    house: str
    flat: int
    comment: str
    show_on_site: bool
    photos: list[str]

    def to_payload(self) -> dict:
        return {
            "UserId": self.user_id,
            "ProblemId": self.problem_id,
            "ReasonId": self.reason_id,
            "CityId": self.city_id,
            "StreetId": self.street_id,
            "House": self.house,
            "Flat": self.flat,
            "Comment": self.comment,
            "ShowOnSite": self.show_on_site,
            "Photos": self.photos,
        }
