from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class EmailDto(AbstractDto):
    email: str

    def to_payload(self) -> dict:
        return {"Email": self.email}
