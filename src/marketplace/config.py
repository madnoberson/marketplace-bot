import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatalogConfig:
    categories_number_per_page: int


def load_catalog_config() -> CatalogConfig:
    return CatalogConfig(
        categories_number_per_page=int(
            _get_env("CATEGORIES_NUMBER_PER_PAGE"),
        ),
    )


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    db: str


def load_postgres_config() -> PostgresConfig:
    return PostgresConfig(
        host=_get_env("POSTGRES_HOST"),
        port=int(_get_env("POSTGRES_PORT")),
        user=_get_env("POSTGRES_USER"),
        password=_get_env("POSTGRES_PASSWORD"),
        db=_get_env("POSTGRES_DB"),
    )


def _get_env(key: str) -> str:
    value = os.getenv(key, None)
    if not value:
        message = f"Env var {key} is not set"
        raise ValueError(message)
    return value
