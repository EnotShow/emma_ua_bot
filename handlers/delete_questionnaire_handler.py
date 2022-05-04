from language.ua import recovery_questionnaire_keyboard, main_manu_buttons
from language.ua.keyboards import *
from language.ua.text import *
from states import FSMDelete, FSMEdit, FSMMenu
from bot_create import bot
from database import delete_questionnaire

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext


async def delete_user_questionnaire(message: types.Message, state: FSMContext):
    if message.text == allow_button.text:
        delete_questionnaire(message.from_user.id)
        await state.finish()
        await FSMDelete.recover.set()
        await bot.send_message(message.from_user.id, f'{tdelet1}', reply_markup=recovery_questionnaire_keyboard)
    elif message.text == cancel_button.text:
        await state.finish()
        await FSMMenu.status.set()
        await bot.send_message(
            message.from_user.id,
            f'{tfind5}',
            reply_markup=main_manu_buttons
        )


async def recover(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMEdit.age.set()
    await bot.send_message(message.from_user.id, f'{tdelet2}', reply_markup=ReplyKeyboardRemove())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_user_questionnaire, state=FSMDelete.status)
    dp.register_message_handler(recover, state=FSMDelete.recover)
