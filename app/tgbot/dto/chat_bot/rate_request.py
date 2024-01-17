from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class RateRequestDto(AbstractDto):
    request_id: int
    mark: int
    comment: str

    def to_payload(self) -> dict:
        return {
            "RequestId": self.request_id,
            "Mark": self.mark,
            "Comment": self.comment,
        }
