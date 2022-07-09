from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStartFind(StatesGroup):
    not_international = State()
    international = State()


class FSMFind(StatesGroup):
    user = State()
    username = State()
    userlist = State()
    international = State()
    message_international = State()
    not_international = State()
    message_not_international = State()


class FSMFindSwitchToInternational(StatesGroup):
    status = State()
