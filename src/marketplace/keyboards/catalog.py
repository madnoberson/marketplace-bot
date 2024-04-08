import math
from typing import Sequence

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from marketplace.callbacks import catalog as callbacks
from marketplace.callbacks.do_nothing import DoNothing
from marketplace.entities.category import Category
from marketplace.entities.subcategory import Subcategory
from marketplace.entities.product import Product


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
            page=1,
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

    if current_page == pages_total_number:
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

    return builder.as_markup()


def get_subcategories(
    subcategories: Sequence[Subcategory],
    category_id: int,
    subcategories_total_number: int,
    subcategories_number_per_page: int,
    current_page: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if len(subcategories) > subcategories_number_per_page:
        message = (
            "Actual number of subcategories greater than"
            "specified number of subcategories per page"
        )
        raise ValueError(message)

    for subcategory in subcategories:
        callback_data = callbacks.GetProduct(
            subcategory_id=subcategory.id,
            product_number=1,
        )
        builder.button(
            text=subcategory.name,
            callback_data=callback_data,
        )
    builder.adjust(3, repeat=True)

    pages_total_number = (
        math.ceil(subcategories_total_number / subcategories_number_per_page)
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
            callback_data=callbacks.GetSubcategories(
                page=previous_page_number,
                category_id=category_id,
            ).pack(),
        )

    if current_page == pages_total_number:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=DoNothing().pack(),
        )
    else:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=callbacks.GetSubcategories(
                page=next_page_number,
                category_id=category_id,
            ).pack(),
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

    return builder.as_markup()


def get_product(
    product: Product,
    subcategory_id: int,
    products_total_number: int,
    current_number: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    previous_product_number = current_number - 1
    next_product_number = current_number + 1

    if previous_product_number == 0:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=DoNothing().pack(),
        )
    else:
        previous_page_button = InlineKeyboardButton(
            text="⏪",
            callback_data=callbacks.GetProduct(
                subcategory_id=subcategory_id,
                product_number=previous_product_number,
            ).pack(),
        )

    if current_number == products_total_number:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=DoNothing().pack(),
        )
    else:
        next_page_button = InlineKeyboardButton(
            text="⏩",
            callback_data=callbacks.GetProduct(
                subcategory_id=subcategory_id,
                product_number=next_product_number,
            ).pack(),
        )

    pages_information_button = InlineKeyboardButton(
        text=f"{current_number}/{products_total_number}",
        callback_data=DoNothing().pack(),
    )
    add_to_cart_button = InlineKeyboardButton(
        text="🛒",
        callback_data=callbacks.ChooseProductQuantity(
            product_id=product.id,
        ).pack(),
    )

    builder.row(
        previous_page_button,
        pages_information_button,
        next_page_button,
        add_to_cart_button,
        width=4,
    )

    return builder.as_markup()


def confirm_adding_product_to_cart(
    product_id: int,
    quantity: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅",
        callback_data=callbacks.AddProductToCart(
            product_id=product_id,
            quantity=quantity,
        ),
    )

    return builder.as_markup()
