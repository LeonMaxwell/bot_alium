from aiogram.dispatcher.filters.state import State, StatesGroup


class Power(StatesGroup):
    activate = State()
    input_code = State()
    error = State()
    close = State()