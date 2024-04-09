from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Product:
    id: int
    name: str
    description: str
    quantity: int
    price: int
    photo_url: Optional[str]
