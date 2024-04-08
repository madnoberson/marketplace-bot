from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product:
    id: int
    name: str
    description: str
    quantity: int
