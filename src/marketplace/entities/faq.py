from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FAQ:
    id: int
    question: str
    answer: int
