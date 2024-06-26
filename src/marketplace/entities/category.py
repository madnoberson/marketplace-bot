from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Category:
    id: int
    name: str
