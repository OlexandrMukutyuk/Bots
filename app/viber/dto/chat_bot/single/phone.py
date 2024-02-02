import re
from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class PhoneDto(AbstractDto):
    phone: str

    def to_payload(self) -> dict:
        pattern = r"\+{0,1}38"

        phone = re.split(pattern, self.phone)[1]

        return {
            "phoneNumber": phone
        }
