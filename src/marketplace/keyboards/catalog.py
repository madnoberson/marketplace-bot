import math
from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from marketplace.callbacks import catalog as callbacks
from marketplace.callbacks.do_nothing import DoNothing
from marketplace.entities.category import Category


def get_categories(
    categories: Sequence[Category],
    categories_total_number: int,
    categories_number_per_page: int,
    current_page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if len(categories) > categories_number_per_page:
        message = (
            "Actual number of categories greater than"
            "specified number of categories per page"
        )
        raise ValueError(message)

    for category in categories:
        callback_data = callbacks.GetSubcategories(
            category_id=category.id,
        )
        builder.button(
            text=category.name,
            callback_data=callback_data,
        )
    builder.adjust(3, repeat=True)

    pages_total_number = (
        math.ceil(categories_total_number / categories_number_per_page)
    )
    previous_page_number = current_page - 1
    next_page_number = current_page + 1

    if previous_page_number == 0:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=DoNothing().pack(),
        )
    else:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=callbacks.GetCategories(page=previous_page_number).pack(),
        )

    if next_page_number == pages_total_number:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=DoNothing().pack(),
        )
    else:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=callbacks.GetCategories(page=next_page_number).pack(),
        )

    pages_information_button = InlineKeyboardButton(
        text=f"{current_page}/{pages_total_number}",
        callback_data=DoNothing().pack(),
    )

    builder.row(
        previous_page_button,
        pages_information_button,
        next_page_button,
        width=3,
    )

    return builder.as_markup(row_width=3)