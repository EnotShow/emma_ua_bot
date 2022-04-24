from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMBan(StatesGroup):
    status = State()
