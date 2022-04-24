from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMRegister(StatesGroup):
    age = State()
    sex = State()
    name = State()
    city = State()
    find = State()
    about = State()
    photo = State()
    some = State()
