from dataclasses import dataclass
from typing import Optional

from marketplace.entities.product import Product
from marketplace.database.sqlalchemy.mappers import ProductMapper


@dataclass(frozen=True, slots=True)
class GetProductResult:
    product: Optional[Product]
    total_number: int


class GetProduct:
    def __init__(self, product_mapper: ProductMapper) -> None:
        self._product_mapper = product_mapper

    async def __call__(
        self,
        *,
        subcategory_id: int,
        number: int,
    ) -> GetProductResult:
        product = await self._product_mapper.with_subcategory_id_and_number(
            subcategory_id=subcategory_id,
            number=number,
        )
        total_number = await self._product_mapper.count_with_subcategory_id(
            subcategory_id=subcategory_id,
        )

        return GetProductResult(
            product=product,
            total_number=total_number,
        )
