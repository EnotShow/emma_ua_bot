from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMWatchList(StatesGroup):
    user = State()
    username = State()

