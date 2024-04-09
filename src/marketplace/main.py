import asyncio
import os
import logging
from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncConnection,
    create_async_engine,
)
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.aiogram import setup_dishka

from marketplace.handlers.catalog import catalog_router
from marketplace.handlers.cart import cart_router
from marketplace.handlers.faq import faq_router
from marketplace.database.sqlalchemy.mappers import (
    CategoryMapper,
    SubcategoryMapper,
    ProductMapper,
    CartItemMapper,
)
from .config import (
    PostgresConfig,
    CatalogConfig,
    load_postgres_config,
    load_catalog_config,
)


class DependenciesProvider(Provider):
    def __init__(
        self,
        postgres_config: PostgresConfig,
        catalog_config: CatalogConfig,
    ) -> None:
        self._postgres_config = postgres_config
        self._catalog_config = catalog_config
        super().__init__()

    @provide(scope=Scope.APP)
    def sqlaclhemy_engine(self) -> AsyncEngine:
        url = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self._postgres_config.user,
            self._postgres_config.password,
            self._postgres_config.host,
            self._postgres_config.port,
            self._postgres_config.db,
        )
        return create_async_engine(url)

    @provide(scope=Scope.REQUEST)
    async def sqlalchemy_connection(
        self,
        sqlalchemy_engine: AsyncEngine,
    ) -> AsyncIterable[AsyncConnection]:
        async with sqlalchemy_engine.connect() as conn:
            yield conn

    @provide(scope=Scope.APP)
    def catalog_config(self) -> CatalogConfig:
        return self._catalog_config

    category_mapper = provide(
        CategoryMapper,
        scope=Scope.REQUEST,
        provides=CategoryMapper,
    )
    subcategory_mapper = provide(
        SubcategoryMapper,
        scope=Scope.REQUEST,
        provides=SubcategoryMapper,
    )
    product_mapper = provide(
        ProductMapper,
        scope=Scope.REQUEST,
        provides=ProductMapper,
    )
    cart_item_mapper = provide(
        CartItemMapper,
        scope=Scope.REQUEST,
        provides=CartItemMapper,
    )


async def main() -> None:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError(f"Env var BOT_TOKEN is not set")

    logging.basicConfig(level=logging.INFO)

    dispatcher = Dispatcher()
    dispatcher.include_routers(catalog_router, cart_router)
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    provider = DependenciesProvider(
        postgres_config=load_postgres_config(),
        catalog_config=load_catalog_config(),
    )
    container = make_async_container(provider)
    setup_dishka(container=container, router=dispatcher)

    await dispatcher.start_polling(bot)


asyncio.run(main())
