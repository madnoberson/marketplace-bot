from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class CartItem:
    id: Optional[int]
    user_id: int
    product_id: int
    quantity: int
