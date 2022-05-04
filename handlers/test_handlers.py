from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot_create import bot
from states import FSMTest

b1 = KeyboardButton('Next')
b = ReplyKeyboardMarkup(resize_keyboard=True).add(b1)


async def test1(message: types.Message, state: FSMContext):
    await FSMTest.status.set()
    async with state.proxy() as data:
        data['status'] = ['some1', 'some2', 'some3', 'some4']
    await bot.send_message(message.from_user.id, 'some', reply_markup=b)


async def test2(message: types.Message, state: FSMContext):
    if message.text == b1.text:
        async with state.proxy() as data:
            for i in data['status']:
                await bot.send_message(message.from_user.id, f'{i}')
    await state.finish()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(test1, commands=['test'])
    dp.register_message_handler(test2, state=FSMTest.status)

