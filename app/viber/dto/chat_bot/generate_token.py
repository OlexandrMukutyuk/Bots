from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class GenerateTokenDto(AbstractDto):
    username: str
    password: str

    def to_payload(self) -> dict:
        return {
            "UserName": self.username,
            "Password": self.password,
            "Status": "string"
        }
