from marketplace.entities.product import Product
from marketplace.entities.cart_item import CartItem
from marketplace.database.sqlalchemy.mappers import CartItemMapper


class AddProductToCart:
    def __init__(self, cart_item_mapper: CartItemMapper) -> None:
        self._cart_item_mapper = cart_item_mapper

    async def __call__(
        self,
        product: Product,
        quantity: int,
        user_id: int,
    ) -> int:
        cart_item = CartItem(
            id=None,
            user_id=user_id,
            product_id=product.id,
            quantity=quantity,
        )
        return await self._cart_item_mapper.save(cart_item)
