import re

from aiogram import types, Dispatcher
from sqlalchemy import select
from sqlalchemy.orm import Session

from admin import admin_chat_id
from bot_create import bot
from bot_create import dp as dispatcher
from database.database import engine, Questionnaire, DBSession


def ban(user_id):
    session = DBSession()
    stmt = select(Questionnaire).where(Questionnaire.user_id == user_id)
    user = session.scalars(stmt).one()
    user.is_banned = True
    session.add(user)
    session.commit()


async def message_to_deleted_users(message: types.Message):
    if message.chat.id == admin_chat_id:
        message_to_send = message.get_args()
        stmt = select(Questionnaire).where(Questionnaire.is_delete == True, Questionnaire.is_banned == False)
        result = engine.connect().execute(stmt).fetchall()
        await bot.delete_message(message.chat.id, message.message_id)
        for user in result:
            try:
                await bot.send_message(user.user_id, message_to_send)
            except:
                pass
        await bot.send_message(message.chat.id, 'Сообщения доставлены')


async def message_to_user(message: types.Message):
    if message.chat.id == admin_chat_id:
        try:
            username = re.findall(f'^@.+,', message.get_args())
            username = f'{username[0]}'.replace('@', '').replace(',', '')
            message_to_send = f'{message.get_args()}'
            message_to_send = message_to_send.lstrip(f'@{username}, ')
            stmt = select(Questionnaire.user_id).where(Questionnaire.username == username)
            user_id = engine.connect().execute(stmt).fetchone()
            await bot.send_message(user_id[0], f'Повідомлення від адміністрації:\n\n{message_to_send}')
            await bot.send_message(message.chat.id, 'Cообщения отправленно')
            await bot.delete_message(message.chat.id, message.message_id)
        except:
            await bot.send_message(message.chat.id, 'Случилась ошибка. Вы ввели неправильный формат или '
                                                    'пользователь заблокировал бота.')
            await bot.delete_message(message.chat.id, message.message_id)


async def announcement(message: types.Message):
    if message.chat.id == admin_chat_id:
        message_to_send = message.get_args()
        stmt = select(Questionnaire).where(Questionnaire.is_delete == False, Questionnaire.is_banned == False)
        result = engine.connect().execute(stmt).fetchall()
        await bot.delete_message(message.chat.id, message.message_id)
        for user in result:
            try:
                await bot.send_message(user.user_id, message_to_send)
            except:
                pass
        await bot.send_message(message.chat.id, 'Сообщения доставлены')


async def send_registered_user_count(message: types.Message):
    if message.chat.id == admin_chat_id:
        stmt = select(Questionnaire).where(-Questionnaire.id)
        result = engine.connect().execute(stmt).fetchall()[-1]
        await bot.send_message(message.chat.id, f'Количество зарегистрированных пользователей {result.id}')


async def stop_bot(message: types.Message):
    if message.chat.id == admin_chat_id:
        await bot.send_message(message.chat.id, 'Бот остановлен !')
        print("Бот остановлен !")
        dispatcher.stop_polling()
        return quit()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(announcement, commands=['announcement'])
    dp.register_message_handler(message_to_user, commands=['message'])
    dp.register_message_handler(message_to_deleted_users, commands=['to_deleted'])
    dp.register_message_handler(send_registered_user_count, commands=['users'])
    dp.register_message_handler(stop_bot, commands=['stop_bot'])
