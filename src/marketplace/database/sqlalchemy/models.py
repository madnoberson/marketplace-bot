from uuid import UUID

from sqlalchemy import MetaData, ForeignKey
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

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )


class SubcategoryModel(Model):
    __tablename__ = "subcategories"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(
        unique=True,
    )
