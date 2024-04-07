from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Category:
    id: UUID
    name: str
