from aiogram.fsm.state import StatesGroup, State


class CreateOrder(StatesGroup):
    enter_full_name = State()
    enter_address = State()
