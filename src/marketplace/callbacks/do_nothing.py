from aiogram.filters.callback_data import CallbackData


class DoNothing(
    CallbackData,
    prefix="do_nothing",
):
    ...
