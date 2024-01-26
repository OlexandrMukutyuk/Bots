from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class ReportIssueDto(AbstractDto):
    user_id: int
    comment: str

    def to_payload(self) -> dict:
        return {"UserId": self.user_id, "Comment": self.comment}
