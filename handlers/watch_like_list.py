from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy import select

from bot_create import bot
from database import is_registered, give_user_who_like, user_questionnaire_template
from database.database import Questionnaire, engine
from keyboards import *
from states import FSMWatchList, FSMMenu


async def watch_next(message: types.Message, state: FSMContext):
    if message.text == 'Закінчити перегляд':
        await state.finish()
        await FSMMenu.status.set()
        await bot.send_message(message.from_user.id, 'Що далі?', reply_markup=main_manu_buttons)
    elif message.text == '💙' or '❌':
        async with state.proxy() as data:
            if message.text == '💙':
                result = engine.connect().execute(select(Questionnaire).where(Questionnaire.user_id == message.from_user.id)).fetchone()
                current_user_username = message.from_user.username
                await bot.send_photo(
                    data['user_id'],
                    result.photo,
                    caption=f"У вас взаємна симпатія з:\n\n{result.about}.\n\nЙого телеграм: @{current_user_username}")

                await bot.send_message(message.from_user.id, f'Ось телеграм цього користувача: @{data["username"]}'
                                                             f'.\nПриємного спілкування.')
            if message.text == '❌':
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
                                f'\n\nОн оставил сообщенния:\n{user_message}',
                        reply_markup=wlbutton
                    )
            except:
                await state.finish()
                await FSMMenu.status.set()
                await bot.send_message(
                    message.from_user.id,
                    'У вас більше немає симпатій.',
                    reply_markup=main_manu_buttons
                )


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(watch_next, state=FSMWatchList.user)
