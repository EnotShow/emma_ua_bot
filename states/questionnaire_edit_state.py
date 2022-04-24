from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMEdit(StatesGroup):
    age = State()
    sex = State()
    name = State()
    city = State()
    find = State()
    about = State()
    photo = State()
