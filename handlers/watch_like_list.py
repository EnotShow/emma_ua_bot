from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy import select

from bot_create import bot
from database import give_user_who_like
from database.database import Questionnaire, engine
from language.ua import *
from language.ua.keyboards import *
from states import FSMWatchList, FSMMenu


async def watch_next(message: types.Message, state: FSMContext):
    if message.text == exit_query.text:
        await state.finish()
        await FSMMenu.status.set()
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)
    elif message.text == like.text or cancel_button.text:
        async with state.proxy() as data:
            if message.text == like.text:
                result = engine.connect().execute(select(Questionnaire).where(Questionnaire.user_id == message.from_user.id)).fetchone()
                current_user_username = message.from_user.username
                await bot.send_photo(
                    data['user_id'],
                    result.photo,
                    caption=f"{tlike1}{result.about}.\n\n{tlike2}{current_user_username}")

                await bot.send_message(message.from_user.id, f'{tlike3}{data["username"]}.{tlike4}')
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
                await FSMMenu.status.set()
                await bot.send_message(
                    message.from_user.id,
                    f'{tlike5}',
                    reply_markup=main_manu_buttons
                )


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(watch_next, state=FSMWatchList.user)
