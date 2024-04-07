from dataclasses import dataclass

from marketplace.entities.category import Category
from marketplace.database.sqlalchemy.mappers import CategoryMapper


@dataclass(frozen=True, slots=True)
class GetCategoriesResult:
    categories: list[Category]
    total_number: int


class GetCategories:
    def __init__(self, category_mapper: CategoryMapper) -> None:
        self._category_mapper = category_mapper

    async def __call__(
        self,
        *,
        limit: int,
        offset: int,
    ) -> GetCategoriesResult:
        categories = await self._category_mapper.list(
            limit=limit,
            offset=offset,
        )
        total_number = await self._category_mapper.count()

        return GetCategoriesResult(
            categories=categories,
            total_number=total_number,
        )
