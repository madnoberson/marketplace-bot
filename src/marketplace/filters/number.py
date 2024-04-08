from aiogram.filters import Filter
from aiogram.types import Message


class IsNumber(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return all(
            map(lambda string: string.isdigit(), message.text),
        )


class IsNotNumber(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return True
        return any(
            map(lambda string: not string.isdigit(), message.text),
        )


class IsNumberGreaterThan(Filter):
    def __init__(self, greater_than: int) -> None:
        self._greater_than = greater_than

    async def __call__(self, message: Message) -> bool:
        return int(message.text) > self._greater_than


class IsNumberLessThan(Filter):
    def __init__(self, less_than: int) -> None:
        self._less_than = less_than

    async def __call__(self, message: Message) -> bool:
        return int(message.text) < self._less_than
