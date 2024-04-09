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
    cart_item_number: int


class StartCreatingOrder(
    CallbackData,
    prefix="start_creating_order",
):
    ...


class CreateOrder(
    CallbackData,
    prefix="create_order",
):
    ...
