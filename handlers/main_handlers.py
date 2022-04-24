from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import random

from bot_create import bot
from keyboards import *
from database import *
from states import *


async def send_welcome(message: types.Message):
    try:
        is_register = is_registered(message.from_user.id)
        if is_banned(message.from_user.id):
            await bot.send_message(
                message.from_user.id,
                'Ви заблоковані. Це рішення не підглядає оскарженню.',
                reply_markup=ReplyKeyboardRemove()
            )
            await FSMBan.status.set()
        else:
            if is_register.is_delete:
                await FSMDelete.recover.set()
                await bot.send_message(
                    message.from_user.id,
                    'Раді бачити вас знову. Бажаєте відновити вашу анкету?',
                    reply_markup=recovery_questionnaire_keyboard
                )
            elif not is_register.is_delete:
                await bot.send_message(
                    message.from_user.id,
                    "Привіт, що тебе цікавить сьогодні?",
                    reply_markup=main_manu_buttons
                )
                await FSMMenu.status.set()
    except:
        await FSMRegister.age.set()
        await bot.send_message(
            message.from_user.id,
            'Хелоу! Давай спершу зареєструєм твою анкету.\n\n'
            'Cкільки землю топчеш?',
        )
    await message.delete()


async def make_chose(message: types.Message, state: FSMContext):
    if is_banned(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Ви заблоковані. Це рішення не підглядає оскарженню.')
        await FSMBan.status.set()
    else:
        try:
            if message.text == 'Знайомитись ☘️':
                await state.finish()
                await FSMFind.user.set()
                related_users = get_related_users(message.from_user.id)
                user_questionnaire = random.choice(related_users)
                async with state.proxy() as data:
                    data['user'] = user_questionnaire.user_id
                await bot.send_photo(
                    message.from_user.id,
                    user_questionnaire.photo,
                    caption=f'{user_questionnaire.about}',
                    reply_markup=fbuttons)
        except IndexError:
            await bot.send_message(message.from_user.id, 'Поки що немає користувачів які підходять вам')
            await state.finish()
            await FSMMenu.status.set()

    if message.text == 'Кому я сподобався':
        try:
            await state.finish()
            await FSMWatchList.user.set()
            questionnaire, user_message = give_user_who_like(message.from_user.id)
            about = f'{questionnaire.about}'
            async with state.proxy() as data:
                data['user_id'] = questionnaire.user_id
                data['username'] = questionnaire.username
                if str(user_message) == 'None':
                    await bot.send_photo(
                        message.from_user.id,
                        questionnaire.photo,
                        caption=about,
                        reply_markup=wlbutton
                    )
                else:
                    await bot.send_photo(
                        message.from_user.id,
                        questionnaire.photo,
                        caption=f'{questionnaire.about}'
                                f'\n\nОн оставил сообщенния:\n{user_message}',
                        reply_markup=wlbutton
                    )
        except:
            await state.finish()
            await FSMMenu.status.set()
            await bot.send_message(
                message.from_user.id,
                "У вас поки що немає симпатій, ми сповістим вас як тільки вони з'являться"
            )

    if message.text == 'Редагувати мою анкету':
        await state.finish()
        await bot.send_message(message.from_user.id, 'Скільки тобі років?')
        await FSMEdit.age.set()

    if message.text == 'Видалити мою анкету':
        await state.finish()
        await FSMDelete.status.set()
        delete_questionnaire(message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            'Ви справді бажаєте видалити вашу анкету?',
            reply_markup=confirmation_button
        )


async def ban(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ви заблоковані, це рішення не підглядає оскарженню.')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(make_chose, state=FSMMenu.status)
    dp.register_message_handler(ban, state=FSMBan.status)
