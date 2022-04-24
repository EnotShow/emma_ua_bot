from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMFind(StatesGroup):
    user = State()
    message = State()
    username = State()
