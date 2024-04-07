from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from marketplace.entities.category import Category
from .models import CategoryModel


class CategoryMapper:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def list(
        self,
        *,
        limit: int,
        offset: int,
    ) -> list[Category]:
        statement = (
            select(CategoryModel)
            .limit(limit)
            .offset(offset)
        )
        rows = (
            await self._connection.execute(statement)
        ).fetchall()

        return [self._to_entity(row) for row in rows]

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
        )
