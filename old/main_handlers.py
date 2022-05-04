import random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot_create import bot
from database import *
from database import _user_selector_algorith
from language.ua.keyboards import *
from language.ua.text import *
from states import *


async def send_welcome(message: types.Message):
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
                await FSMDelete.recover.set()
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
                await FSMMenu.status.set()
    except:
        # У пользователя нет анкеты
        await FSMRegister.age.set()
        await bot.send_message(
            message.from_user.id,
            f'{tmain8}',
        )
    await message.delete()


async def make_chose(message: types.Message, state: FSMContext):
    if not check_username(message.from_user.id):
        await bot.send_message(message.from_user.id, f'{no_username}')

    # if return_to_main_manu(message.text):
    #     await send_welcome(message.text)
    # else:
    # Проверяет забаненый ли пользователь
    if is_banned(message.from_user.id):
        await bot.send_message(message.from_user.id, f'{tmain1}')
        await FSMBan.status.set()
    else:
        try:
            # Знайомитись
            if message.text == b1.text:
                await state.finish()
                await FSMFind.user.set()
                # -------------
                user_questionnaire = await _user_selector_algorith(
                    message.from_user.id,
                    get_related_users(message.from_user.id),
                    state
                )
                # related_users = get_related_users(message.from_user.id)
                # if len(related_users) == 1:
                #     related_users = related_users[0]
                # user_questionnaire = random.choice(related_users)
                # async with state.proxy() as data:
                #     data['userlist'] = related_users.remove(user_questionnaire)
                #     data['user'] = user_questionnaire.user_id
                # # ------------
                await bot.send_photo(
                    message.from_user.id,
                    user_questionnaire.photo,
                    caption=f'{user_questionnaire.about}',
                    reply_markup=fbuttons)
        except IndexError:
            await bot.send_message(message.from_user.id, f'{tmain5}')
            await state.finish()
            await FSMMenu.status.set()

    # Кому я сподобався
    if message.text == b2.text:
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
                                f'{tedit6}\n{user_message}',
                        reply_markup=wlbutton
                    )
        except:
            await state.finish()
            await FSMMenu.status.set()
            await bot.send_message(
                message.from_user.id,
                f"{tmain7}"
            )
    # Редагувати мою анкету
    if message.text == b3.text:
        await state.finish()
        await FSMPreEdit.state_one.set()
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=editk1)

    # Видалити мою анкету
    if message.text == b4.text:
        await state.finish()
        await FSMDelete.status.set()
        await bot.send_message(
            message.from_user.id,
            f'{tmain9}',
            reply_markup=confirmation_button
        )


async def ban(message: types.Message):
    await bot.send_message(message.from_user.id, f'{tmain1}')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(make_chose, state=FSMMenu.status)
    dp.register_message_handler(ban, state=FSMBan.status)
