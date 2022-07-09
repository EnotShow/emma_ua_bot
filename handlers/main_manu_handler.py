from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.orm import Session

from bot_create import bot
from database import *
from database.database import engine
from handlers.quistennaire_find_handler import start_not_international_search
from language.ua.keyboards import *
from language.ua.text import *
from states import *


async def make_chose(message: types.Message, state: FSMContext):
    """
    Каша из кода)))
    """
    # Проверяет забаненый ли пользователь
    if is_banned(message.from_user.id):
        await bot.send_message(message.from_user.id, f'{tmain1}')
        await FSMBan.status.set()

    else:
        # Знайомитись
        if message.text == b1.text:
            await start_not_international_search(message, state)

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
                                f'{tmain6}\n{user_message}',
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
        await bot.send_message(message.from_user.id, f'{tmain4}', reply_markup=ReplyKeyboardRemove())
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


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(make_chose)
