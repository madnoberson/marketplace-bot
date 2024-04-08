from aiogram.fsm.state import StatesGroup, State


class AddToCart(StatesGroup):
    confirm = State()
