from sqlalchemy import select, text
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

    async def count(self) -> int:
        statement = text("SELECT COUNT(c.*) FROM categories c")
        return (await self._connection.execute(statement)).scalar_one()

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
        )
