from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RateEnterpriseGuestDto(AbstractDto):
    guest_id: str
    enterprise_id: int
    rate: int
    # comment: str

    def to_payload(self) -> dict:
        return {
            "GuestId": self.guest_id,
            "KpId": self.enterprise_id,
            "Rate": self.rate,
        }
