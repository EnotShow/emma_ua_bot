from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMMenu(StatesGroup):
    status = State()
