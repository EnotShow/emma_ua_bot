from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMTest(StatesGroup):
    status = State()
