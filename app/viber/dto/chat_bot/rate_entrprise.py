from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RateEnterpriseDto(AbstractDto):
    user_id: str
    enterprise_id: int
    rate: int
    # comment: str

    def to_payload(self) -> dict:
        return {
            "UserId": self.user_id,
            "KpId": self.enterprise_id,
            "Rate": self.rate,
            # "Comment": self.comment,
        }
