from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy import select

from bot_create import bot
from database import give_user_who_like
from database.database import Questionnaire, engine
from database.responses import check_country
from handlers.welcome_handlers import send_welcome
from language.ua.keyboards import *
from language.ua.text import *
from states import FSMWatchList


async def watch_next(message: types.Message, state: FSMContext):
    """
    Получает следующего пользователя из списка пользователуй, которым понравился пользователь
    """
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        if message.text == exit_query.text:
            await state.finish()
            await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)
        elif message.text == like.text or cancel_button.text:
            async with state.proxy() as data:
                if message.text == like.text:
                    try:
                        result = engine.connect().execute(
                            select(Questionnaire).where(Questionnaire.user_id == message.from_user.id)).fetchone()
                        current_user_username = message.from_user.username
                        await bot.send_photo(
                            data['user_id'],
                            result.photo,
                            caption=f"{tlike1}{result.about}.\n\n{tlike2}{current_user_username}")
                        if check_country(data['user_id']) == 'Україна':
                            await bot.send_message(data['user_id'], warning)

                        await bot.send_message(message.from_user.id, f'{tlike3}{data["username"]}.{tlike4}')
                        if check_country(message.from_user.id) == 'Україна':
                            await bot.send_message(message.from_user.id, warning)
                    except:
                        await bot.send_message(message.from_user.id, f'{tfind6}')

                if message.text == dislike.text:
                    pass
                try:
                    questionnaire, user_message = give_user_who_like(message.from_user.id)
                    about = f'{questionnaire.about}'
                    data['user_id'] = questionnaire.user_id
                    data['username'] = questionnaire.username
                    if str(user_message) == 'None':
                        await bot.send_photo(
                            message.from_user.id,
                            questionnaire.photo,
                            caption=f'{questionnaire.about}',
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
                        f'{tlike5}',
                        reply_markup=main_manu_buttons
                    )


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(watch_next, state=FSMWatchList.user)
