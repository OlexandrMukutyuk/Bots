from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RegisterDto(AbstractDto):
    first_name: str
    last_name: str
    middle_name: str
    gender: str
    phone: str
    city_id: int
    street_id: int
    house: str
    flat: int
    password: str
    email: str

    def to_payload(self) -> dict:
        return {
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "MiddleName": self.middle_name,
            "Gender": self.gender,
            "Phone": self.phone,
            "CityId": self.city_id,
            "StreetId": self.street_id,
            "House": self.house,
            "Flat": self.flat,
            "Password": self.password,
            "Email": self.email,
        }
