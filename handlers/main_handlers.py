import random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.orm import Session

from bot_create import bot
from database import *
from database.database import engine
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


# async def some(message: types.Message):
#     if message.text == 'some':
#         await bot.send_message(message.from_user.id, 'some')


async def make_chose(message: types.Message, state: FSMContext):
    if not check_username(message.from_user.id):
        await bot.send_message(message.from_user.id, f'{no_username}')

    # Проверяет забаненый ли пользователь
    if is_banned(message.from_user.id):
        await bot.send_message(message.from_user.id, f'{tmain1}')
        await FSMBan.status.set()

    else:
        # Знайомитись
        if message.text == b1.text:
            try:
                await FSMFind.user.set()
                async with state.proxy() as data:
                    related_users = get_related_users(message.from_user.id)
                    if not related_users:
                        related_users = get_related_users(message.from_user.id, region_key=False)
                    if related_users:
                        if len(related_users) == 1:
                            related_users = related_users[0]
                            user_questionnaire = related_users
                        else:
                            user_questionnaire = random.choice(related_users)
                            related_users.remove(user_questionnaire)
                        data['userlist'] = related_users
                        data['user'] = user_questionnaire.user_id
                        await bot.send_photo(
                            message.from_user.id,
                            user_questionnaire.photo,
                            caption=f'{user_questionnaire.about}',
                            reply_markup=fbuttons)
                    else:
                        await state.finish()
                        await bot.send_message(message.from_user.id, f'{tmain5}', reply_markup=main_manu_buttons)
            except IndexError:
                await bot.send_message(message.from_user.id, f'{tmain5}', reply_markup=main_manu_buttons)

    # Кому я сподобався
    if message.text == b2.text:
        try:
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
            await bot.send_message(
                message.from_user.id,
                f"{tmain7}"
            )
    # Редагувати мою анкету
    if message.text == b3.text:
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=editk1)

    # Видалити мою анкету
    if message.text == b4.text:
        await FSMDelete.status.set()
        await bot.send_message(
            message.from_user.id,
            f'{tmain9}',
            reply_markup=confirmation_button
        )
    # -------------------------
    if message.text == editb1.text:
        questionnaire = get_user_questionnaire(message.from_user.id)
        await bot.send_photo(
            message.from_user.id,
            questionnaire.photo,
            caption=f'{questionnaire.about}',
            reply_markup=main_manu_buttons
        )
    if message.text == editb2.text:
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=editk2)
    if message.text == mainb.text:
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)
    if message.text == editb3.text:
        await FSMEdit.age.set()
        await bot.send_message(message.from_user.id, f'{tmain4}')
    elif message.text == editb4.text:
        await FSMPhotoEdit.photo.set()
        await bot.send_message(message.from_user.id, f'{tedit10}', reply_markup=ReplyKeyboardRemove())
    elif message.text == editb5.text:
        await FSMAboutEdit.about.set()
        await bot.send_message(message.from_user.id, f'{tedit11}')
    elif message.text == editb6.text:
        questionnaire = get_user_questionnaire(message.from_user.id)
        with Session(engine) as session:
            questionnaire.username = message.from_user.username
            session.add(questionnaire)
            session.commit()
        await bot.send_message(message.from_user.id, f'{tedit12}', reply_markup=main_manu_buttons)
    # recover
    if message.text == recoverb.text:
        await FSMEdit.age.set()
        await bot.send_message(message.from_user.id, f'{tdelet2}', reply_markup=ReplyKeyboardRemove())


async def ban(message: types.Message):
    await bot.send_message(message.from_user.id, f'{tmain1}')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(make_chose)
    dp.register_message_handler(ban, state=FSMBan.status)
