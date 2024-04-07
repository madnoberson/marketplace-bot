from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class GetCategories(
    CallbackData,
    prefix="get_categories",
):
    page: int


class GetSubcategories(
    CallbackData,
    prefix="get_subcategories",
):
    category_id: UUID
    page: int


class GetProducts(
    CallbackData,
    prefix="get_products",
):
    subcategory_id: UUID
