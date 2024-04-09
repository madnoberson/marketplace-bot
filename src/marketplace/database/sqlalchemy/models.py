from uuid import UUID

from sqlalchemy import MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


convention = {
    "ix": "ix_%(column_0_label)s",  # INDEX
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",  # UNIQUE
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # CHECK
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",  # FOREIGN KEY
    "pk": "pk_%(table_name)s",  # PRIMARY KEY
}


class Model(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class CategoryModel(Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )


class SubcategoryModel(Model):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )


class ProductModel(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey("subcategories.id", ondelete="CASCADE"),
    )
    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]
    poster_url: Mapped[str]


class CartItemModel(Model):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
    )
    user_id: Mapped[int]
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
    )
    quantity: Mapped[int]

    __table_args__ = (UniqueConstraint("user_id", "product_id"),)
