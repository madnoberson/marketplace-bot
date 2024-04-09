from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from marketplace.callbacks import cart as callbacks
from marketplace.callbacks.do_nothing import DoNothing
from marketplace.entities.cart_item import CartItem


def get_cart_item(
    cart_item: CartItem,
    cart_items_total_number: int,
    current_number: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    previous_cart_item_number = current_number - 1
    next_cart_item_number = current_number + 1

    if previous_cart_item_number == 0:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=DoNothing().pack(),
        )
    else:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=callbacks.GetCartItem(
                cart_item_number=previous_cart_item_number,
            ).pack(),
        )

    if current_number == cart_items_total_number:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=DoNothing().pack(),
        )
    else:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=callbacks.GetCartItem(
                cart_item_number=next_cart_item_number,
            ).pack(),
        )

    pages_information_button = InlineKeyboardButton(
        text=f"{current_number}/{cart_items_total_number}",
        callback_data=DoNothing().pack(),
    )
    remove_from_cart_button = InlineKeyboardButton(
        text="🗑",
        callback_data=callbacks.DeleteCartItem(
            cart_item_number=current_number,
        ).pack(),
    )
    create_order_button = InlineKeyboardButton(
        text="📦",
        callback_data=callbacks.StartCreatingOrder().pack(),
    )

    builder.row(
        previous_page_button,
        pages_information_button,
        next_page_button,
        remove_from_cart_button,
        create_order_button,
        width=3,
    )

    return builder.as_markup()


def confirm_creating_order() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅",
        callback_data=callbacks.CreateOrder(),
    )

    return builder.as_markup()
