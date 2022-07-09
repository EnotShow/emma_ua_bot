from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove

from bot_create import bot
from database import *
from language.ua.keyboards import *
from language.ua.text import *
from states import *


async def send_welcome(message: types.Message):
    """
    Отправляет пользователю сообщение в случае команды /start
    """
    try:
        is_register = is_registered(message.from_user.id)
        # Проверяет забаненый ли пользователь
        if is_banned(message.from_user.id):
            await bot.send_message(
                message.from_user.id,
                f'{tmain1}',
                reply_markup=ReplyKeyboardRemove()
            )
            await FSMBan.status.set()
        else:
            # Если пользовтель удалил свою анкету
            if is_register.is_delete:
                await bot.send_message(
                    message.from_user.id,
                    f'{tmain2}',
                    reply_markup=recovery_questionnaire_keyboard
                )
            # Пользователь зарегистрирован
            elif not is_register.is_delete:
                await bot.send_message(
                    message.from_user.id,
                    f'{tmain3}',
                    reply_markup=main_manu_buttons
                )
    except:
        # У пользователя нет анкеты
        await FSMRegister.age.set()
        await bot.send_message(
            message.from_user.id,
            f'{tmain8}',
        )
    await message.delete()


async def ban(message: types.Message):
    await bot.send_message(message.from_user.id, f'{tmain1}')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(ban, state=FSMBan.status)
