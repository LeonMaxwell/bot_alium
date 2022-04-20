from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateCharacters(StatesGroup):
    start = State()
    login = State()
    create = State()