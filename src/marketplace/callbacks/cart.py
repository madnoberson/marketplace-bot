from aiogram.filters.callback_data import CallbackData


class GetCartItem(
    CallbackData,
    prefix="get_cart_item",
):
    cart_item_number: int


class DeleteCartItem(
    CallbackData,
    prefix="delete_cart_item",
):
    cart_item_id: int
