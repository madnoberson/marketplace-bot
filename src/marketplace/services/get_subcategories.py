from dataclasses import dataclass
from uuid import UUID

from marketplace.entities.subcategory import Subcategory
from marketplace.database.sqlalchemy.mappers import SubcategoryMapper


@dataclass(frozen=True, slots=True)
class GetSubcategoriesResult:
    subcategories: list[Subcategory]
    total_number: int


class GetSubcategories:
    def __init__(self, subcategory_mapper: SubcategoryMapper) -> None:
        self._subcategory_mapper = subcategory_mapper

    async def __call__(
        self,
        *,
        category_id: int,
        limit: int,
        offset: int,
    ) -> GetSubcategoriesResult:
        subcategories = await self._subcategory_mapper.list_with_category_id(
            category_id=category_id,
            limit=limit,
            offset=offset,
        )
        total_number = await self._subcategory_mapper.count_with_category_id(
            category_id=category_id,
        )

        return GetSubcategoriesResult(
            subcategories=subcategories,
            total_number=total_number,
        )
