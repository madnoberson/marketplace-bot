from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.keyboards import catalog as keyboards
from marketplace.callbacks import catalog as callbacks
from marketplace.states import catalog as states
from marketplace.config import CatalogConfig
from marketplace.services.get_categories import GetCategories
from marketplace.services.get_subcategories import GetSubcategories
from marketplace.services.get_product import GetProduct
from marketplace.services.acquire_product import AcquireProduct


catalog_router = Router()


@catalog_router.message(Command("catalog"))
@inject
async def get_categories(
    message: Message,
    catalog_config: FromDishka[CatalogConfig],
    get_categories: FromDishka[GetCategories],
) -> None:
    get_categories_result = await get_categories(
        limit=catalog_config.categories_number_per_page,
        offset=0,
    )
    reply_markup = keyboards.get_categories(
        categories=get_categories_result.categories,
        categories_total_number=get_categories_result.total_number,
        categories_number_per_page=catalog_config.categories_number_per_page,
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
    get_categories: FromDishka[GetCategories],
) -> None:
    get_categories_result = await get_categories(
        limit=callback_data.page * (
            catalog_config.categories_number_per_page
        ),
        offset=(callback_data.page - 1) * (
            catalog_config.categories_number_per_page
        ),
    )
    reply_markup = keyboards.get_categories(
        categories=get_categories_result.categories,
        categories_total_number=get_categories_result.total_number,
        categories_number_per_page=catalog_config.categories_number_per_page,
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
    get_subcategories: FromDishka[GetSubcategories],
) -> None:
    get_subcategories_result = await get_subcategories(
        category_id=callback_data.category_id,
        limit=callback_data.page * (
            catalog_config.subcategories_number_per_page
        ),
        offset=(callback_data.page - 1) * (
            catalog_config.subcategories_number_per_page
        ),
    )
    reply_markup = keyboards.get_subcategories(
        subcategories=get_subcategories_result.subcategories,
        category_id=callback_data.category_id,
        subcategories_total_number=(
            get_subcategories_result.total_number
        ),
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
    get_product: FromDishka[GetProduct],
) -> None:
    get_product_result = await get_product(
        subcategory_id=callback_data.subcategory_id,
        number=callback_data.product_number,
    )
    text = (
        "<b>"
        f"Name: {get_product_result.product.name}\n"
        f"Description: {get_product_result.product.description}\n"
        f"Quantity: {get_product_result.product.quantity}"
        "</b>"
    )
    reply_markup = keyboards.get_product(
        product=get_product_result.product,
        subcategory_id=callback_data.subcategory_id,
        products_total_number=get_product_result.total_number,
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
    await state.set_data(
        {
            "product_id": callback_data.product_id,
        },
    )
    await callback.message.answer(text="<b>Choose quantity:</b>")
    await callback.answer()
