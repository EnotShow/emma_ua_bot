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


class FSMPreEdit(StatesGroup):
    state_one = State()
    state_two = State()


class FSMEdit(StatesGroup):
    age = State()
    sex = State()
    name = State()
    city = State()
    find = State()
    about = State()
    photo = State()


class FSMPhotoEdit(StatesGroup):
    photo = State()


class FSMAboutEdit(StatesGroup):
    about = State()


class FSMUsernameEdit(StatesGroup):
    photo = State()
