from aiogram.filters import Filter
from aiogram.types import Message


INTERNATIONAL_FULL_NAME_STRINGS_NUMBER = 2  # John Doe
RUSSIAN_FULL_NAME_STRINGS_NUMBER = 3  # Ivanov Ivan Ivanovich


class IsFullName(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False

        return len(message.text.split(" ")) in (
            INTERNATIONAL_FULL_NAME_STRINGS_NUMBER,
            RUSSIAN_FULL_NAME_STRINGS_NUMBER,
        )


class IsNotFullName(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return True

        return len(message.text.split(" ")) not in (
            INTERNATIONAL_FULL_NAME_STRINGS_NUMBER,
            RUSSIAN_FULL_NAME_STRINGS_NUMBER,
        )


class IsAddress(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.text)


class IsNotAddress(Filter):
    async def __call__(self, message: Message) -> bool:
        return not bool(message.text)
