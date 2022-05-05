from aiogram.dispatcher import FSMContext

from handlers.main_handlers import send_welcome
from language.ua.keyboards import *
from language.ua.text import *
from states import FSMDelete
from bot_create import bot
from database import delete_questionnaire

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove


async def delete_user_questionnaire(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await send_welcome(message)
    else:
        if message.text == allow_button.text:
            delete_questionnaire(message.from_user.id)
            await bot.send_message(message.from_user.id, f'{tdelet1}', reply_markup=recovery_questionnaire_keyboard)
        elif message.text == cancel_button.text:
            await bot.send_message(
                message.from_user.id,
                f'{tfind5}',
                reply_markup=main_manu_buttons
            )
    await state.finish()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_user_questionnaire, state=FSMDelete.status)
