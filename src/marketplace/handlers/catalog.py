from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.keyboards import catalog as keyboards
from marketplace.callbacks import catalog as callbacks
from marketplace.states import catalog as states
from marketplace.config import CatalogConfig
from marketplace.filters.number import (
    IsNumber,
    IsNotNumber,
    IsNumberGreaterThan,
    IsNumberLessThan,
)
from marketplace.database.sqlalchemy.mappers import (
    CategoryMapper,
    SubcategoryMapper,
    ProductMapper,
)


catalog_router = Router()


@catalog_router.message(Command("catalog"))
@inject
async def get_categories(
    message: Message,
    catalog_config: FromDishka[CatalogConfig],
    category_mapper: FromDishka[CategoryMapper],
) -> None:
    categories = await category_mapper.list(
        limit=catalog_config.categories_number_per_page,
        offset=0,
    )
    categories_total_number = await category_mapper.count()

    reply_markup = keyboards.get_categories(
        categories=categories,
        categories_total_number=categories_total_number,
        categories_number_per_page=(
            catalog_config.categories_number_per_page
        ),
        current_page=1,
    )

    await message.answer(
        text="<b>Choose category:</b>",
        reply_markup=reply_markup,
    )


@catalog_router.callback_query(callbacks.GetCategories.filter())
@inject
async def get_categories_with_page(
    callback: CallbackQuery,
    callback_data: callbacks.GetCategories,
    catalog_config: FromDishka[CatalogConfig],
    category_mapper: FromDishka[CategoryMapper],
) -> None:
    categories = await category_mapper.list(
        limit=callback_data.page * (
            catalog_config.categories_number_per_page
        ),
        offset=(callback_data.page - 1) * (
            catalog_config.categories_number_per_page
        ),
    )
    categories_total_number = await category_mapper.count()

    reply_markup = keyboards.get_categories(
        categories=categories,
        categories_total_number=categories_total_number,
        categories_number_per_page=(
            catalog_config.categories_number_per_page
        ),
        current_page=callback_data.page,
    )

    await callback.message.edit_text(
        text="<b>Choose category:</b>",
        reply_markup=reply_markup,
    )


@catalog_router.callback_query(callbacks.GetSubcategories.filter())
@inject
async def get_subcategories(
    callback: CallbackQuery,
    callback_data: callbacks.GetSubcategories,
    catalog_config: FromDishka[CatalogConfig],
    subcategory_mapper: FromDishka[SubcategoryMapper],
) -> None:
    subcategories = await subcategory_mapper.list_with_category_id(
        category_id=callback_data.category_id,
        limit=callback_data.page * (
            catalog_config.subcategories_number_per_page
        ),
        offset=(callback_data.page - 1) * (
            catalog_config.subcategories_number_per_page
        ),
    )
    subcategories_total_number = await subcategory_mapper.count_with_category_id(
        category_id=callback_data.category_id,
    )

    reply_markup = keyboards.get_subcategories(
        subcategories=subcategories,
        category_id=callback_data.category_id,
        subcategories_total_number=subcategories_total_number,
        subcategories_number_per_page=(
            catalog_config.subcategories_number_per_page
        ),
        current_page=1,
    )

    await callback.message.edit_text(
        text="<b>Choose subcategory:</b>",
        reply_markup=reply_markup,
    )


@catalog_router.callback_query(callbacks.GetProduct.filter())
@inject
async def get_product(
    callback: CallbackQuery,
    callback_data: callbacks.GetProduct,
    product_mapper: FromDishka[ProductMapper],
) -> None:
    product = await product_mapper.with_subcategory_id_and_number(
        subcategory_id=callback_data.subcategory_id,
        number=callback_data.product_number,
    )
    products_total_number = await product_mapper.count_with_subcategory_id(
        subcategory_id=callback_data.subcategory_id,
    )

    text = (
        "<b>"
        f"Name: {product.name}\n"
        f"Description: {product.description}\n"
        f"Quantity: {product.quantity} \n"
        f"Price: {product.price}\n"
        "</b>"
    )
    reply_markup = keyboards.get_product(
        product=product,
        subcategory_id=callback_data.subcategory_id,
        products_total_number=products_total_number,
        current_number=callback_data.product_number,
    )

    await callback.message.answer(
        text=text,
        reply_markup=reply_markup,
    )
    await callback.answer()


@catalog_router.callback_query(callbacks.ChooseProductQuantity.filter())
@inject
async def choose_product_quantity(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: callbacks.ChooseProductQuantity,
) -> None:
    await state.set_state(states.AddToCart.confirm)
    await state.set_data({"product_id": callback_data.product_id})
    await callback.message.answer(text="<b>Choose quantity:</b>")
    await callback.answer()


@catalog_router.message(
    states.AddToCart.confirm,
    IsNotNumber(),
)
@catalog_router.message(
    states.AddToCart.confirm,
    IsNumber(),
    IsNumberLessThan(1),
)
async def invalid_product_quantity(message: Message) -> None:
    text = (
        "<b>"
        "Invalid product quantity.\n\n"
        "Please, choose another quantity:"
        "</b>"
    )
    await message.answer(text=text)


@catalog_router.message(
    states.AddToCart.confirm,
    IsNumber(),
    IsNumberGreaterThan(0),
)
@inject
async def confirm_adding_product_to_cart(
    message: Message,
    state: FSMContext,
    product_mapper: FromDishka[ProductMapper],
) -> None:
    state_data = await state.get_data()

    product = await product_mapper.with_id(
        product_id=state_data.get("product_id"),
    )

    product_quantity_user_chose = int(message.text)
    if product_quantity_user_chose > product.quantity:
        text = (
            "<b>"
            f"Only {product.quantity} products is avaliable.\n\n"
            "Please, choose another quantity:"
            "</b>"
        )
        await message.answer(text=text)
    else:
        text = (
            "<b>"
            f"You are going to add {product_quantity_user_chose} "
            f"'{product.name}' to cart.\n\n"
            "Please, confirm."
            "</b>"
        )
        reply_markup = keyboards.confirm_adding_product_to_cart(
            product_id=product.id,
            quantity=product_quantity_user_chose,
        )
        await message.answer(
            text=text,
            reply_markup=reply_markup,
        )
