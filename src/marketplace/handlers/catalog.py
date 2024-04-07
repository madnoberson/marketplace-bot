from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from dishka.integrations.aiogram import FromDishka, inject

from marketplace.keyboards import catalog as keyboards
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

