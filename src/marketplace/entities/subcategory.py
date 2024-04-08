from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Subcategory:
    id: int
    name: str
