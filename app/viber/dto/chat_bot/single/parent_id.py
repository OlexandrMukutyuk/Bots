from dataclasses import dataclass
from typing import Optional

from dto import AbstractDto


@dataclass
class ParentIdDto(AbstractDto):
    parent_id:  Optional[int]

    def to_payload(self) -> dict:
        return {"ParentId": self.parent_id}
