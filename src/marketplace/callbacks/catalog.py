from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class GetSubcategories(
    CallbackData,
    prefix="get_subcategories_of",
):
    category_id: UUID


class GetCategories(
    CallbackData,
    prefix="get_categories",
):
    page: int
