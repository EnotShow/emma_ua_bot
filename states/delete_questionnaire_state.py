from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMDelete(StatesGroup):
    status = State()
    recover = State()