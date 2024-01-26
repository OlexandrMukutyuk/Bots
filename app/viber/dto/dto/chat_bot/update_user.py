from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class UpdateUserDto(AbstractDto):
    user_id: int
    first_name: str
    last_name: str
    middle_name: str
    gender: str
    phone: str
    city_id: int
    street_id: int
    house: str
    flat: int

    def to_payload(self) -> dict:
        return {
            "UserId": self.user_id,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "MiddleName": self.middle_name,
            "Gender": self.gender,
            "Phone": self.phone,
            "CityId": self.city_id,
            "StreetId": self.street_id,
            "House": self.house,
            "Flat": self.flat,
        }
