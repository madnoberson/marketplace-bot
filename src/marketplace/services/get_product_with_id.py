from typing import Optional

from marketplace.entities.product import Product
from marketplace.database.sqlalchemy.mappers import ProductMapper


class GetProductWithId:
    def __init__(self, product_mapper: ProductMapper) -> None:
        self._product_mapper = product_mapper

    async def __call__(self, product_id: int) -> Optional[Product]:
        return await self._product_mapper.with_id(
            product_id=product_id,
        )
