from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from marketplace.entities.category import Category
from marketplace.entities.subcategory import Subcategory
from .models import CategoryModel, SubcategoryModel


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


class SubcategoryMapper:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def list_with_category_id(
        self,
        *,
        category_id: UUID,
        limit: int,
        offset: int,
    ) -> list[Subcategory]:
        statement = (
            select(SubcategoryModel)
            .where(SubcategoryModel.category_id == category_id)
            .limit(limit)
            .offset(offset)
        )
        rows = (
            await self._connection.execute(statement)
        ).fetchall()

        return [self._to_entity(row) for row in rows]

    async def count_with_category_id(self, category_id: UUID) -> int:
        statement = text(
            """
            SELECT COUNT(sc.*)
            FROM subcategories sc
            WHERE sc.category_id = :category_id
            """
        )
        parameters = {"category_id": category_id}

        return (
            await self._connection.execute(statement, parameters)
        ).scalar_one()

    def _to_entity(self, model: SubcategoryModel) -> Subcategory:
        return Subcategory(
            id=model.id,
            name=model.name,
        )
