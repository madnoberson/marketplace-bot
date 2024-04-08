from dataclasses import dataclass

from marketplace.entities.cart_item import CartItem
from marketplace.database.sqlalchemy.mappers import CartItemMapper


@dataclass(frozen=True, slots=True)
class GetCartItemResult:
    cart_item: CartItem
    total_number: int


class GetCartItem:
    def __init__(self, cart_item_mapper: CartItemMapper) -> None:
        self._cart_item_mapper = cart_item_mapper

    async def __call__(
        self,
        *,
        user_id: int,
        number: int,
    ) -> GetCartItemResult:
        cart_item = await self._cart_item_mapper.with_user_id_and_number(
            user_id=user_id,
            number=number,
        )
        total_number = await self._cart_item_mapper.count_with_user_id(
            user_id=user_id,
        )
        return GetCartItemResult(
            cart_item=cart_item,
            total_number=total_number,
        )
