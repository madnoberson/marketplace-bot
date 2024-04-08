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
    category_id: int
    page: int


class GetProduct(
    CallbackData,
    prefix="get_products",
):
    subcategory_id: int
    product_number: int


class ChooseProductQuantity(
    CallbackData,
    prefix="choose_product_quantity",
):
    product_id: int
