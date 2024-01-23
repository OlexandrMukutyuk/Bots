from dataclasses import dataclass

from dto import AbstractDto


@dataclass
class ProblemIdDto(AbstractDto):
    problem_id: int

    def to_payload(self) -> dict:
        return {"ProblemId": self.problem_id}
