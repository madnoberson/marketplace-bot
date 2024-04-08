from typing import Optional

from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncConnection

from marketplace.entities.category import Category
from marketplace.entities.subcategory import Subcategory
from marketplace.entities.product import Product
from marketplace.entities.cart_item import CartItem
from .models import (
    CategoryModel,
    SubcategoryModel,
    ProductModel,
    CartItemModel,
)


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
        category_id: int,
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

    async def count_with_category_id(self, category_id: int) -> int:
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


class ProductMapper:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def with_subcategory_id_and_number(
        self,
        *,
        subcategory_id: int,
        number: int,
    ) -> Optional[Product]:
        statement = (
            select(ProductModel)
            .where(ProductModel.subcategory_id == subcategory_id)
            .limit(number)
            .offset(number - 1)
        )
        row = (
            await self._connection.execute(statement)
        ).fetchone()
        if row:
            return self._to_entity(row)
        return None

    async def with_id(
        self,
        product_id: int,
        acquire: bool = False,
    ) -> Product:
        if acquire:
            statement = (
                select(ProductModel)
                .where(ProductModel.id == product_id)
                .with_for_update()
            )
        else:
            statement = (
                select(ProductModel)
                .where(ProductModel.id == product_id)
            )
        row = (
            await self._connection.execute(statement)
        ).fetchone()
        if row:
            return self._to_entity(row)
        return None

    async def count_with_subcategory_id(
        self,
        subcategory_id: int,
    ) -> int:
        statement = text(
            """
            SELECT COUNT(p.*)
            FROM products p
            WHERE p.subcategory_id = :subcategory_id
            """
        )
        parameters = {"subcategory_id": subcategory_id}

        return (
            await self._connection.execute(statement, parameters)
        ).scalar_one()

    def _to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            quantity=model.quantity,
            price=model.price,
        )


class CartItemMapper:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def save(self, cart_item: CartItem) -> int:
        statement = (
            insert(CartItemModel)
            .values(
                user_id=cart_item.user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
            )
            .returning(CartItemModel.id)
        )
        cart_item_id =  (
            await self._connection.execute(statement)
        ).scalar_one()

        await self._connection.commit()

        return cart_item_id

    async def with_user_id_and_number(
        self,
        *,
        user_id: int,
        number: int,
    ) -> Optional[CartItem]:
        statement = (
            select(CartItemModel)
            .where(CartItemModel.user_id == user_id)
            .limit(number)
            .offset(number - 1)
        )
        row = (
            await self._connection.execute(statement)
        ).fetchone()
        if row:
            return self._to_entity(row)
        return None

    async def count_with_user_id(self, user_id: int) -> int:
        statement = text(
            """
            SELECT COUNT(ci.*)
            FROM cart_items ci
            WHERE ci.user_id = :user_id
            """
        )
        parameters = {"user_id": user_id}

        return (
            await self._connection.execute(statement, parameters)
        ).scalar_one()

    def _to_entity(self, model: CartItemModel) -> CartItem:
        return CartItem(
            id=model.id,
            user_id=model.user_id,
            product_id=model.product_id,
            quantity=model.quantity,
        )
