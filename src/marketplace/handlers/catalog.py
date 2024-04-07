from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.keyboards import catalog as keyboards
from marketplace.callbacks import catalog as callbacks
from marketplace.config import CatalogConfig
from marketplace.services.get_categories import GetCategories


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
        text="Choose category:",
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
        text="Choose category:",
        reply_markup=reply_markup,
    )
