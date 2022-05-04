from aiogram import types, Dispatcher

from aiogram.dispatcher import filters

from bot_create import bot
from .admin_features import ban


async def ban_user(callback_query: types.CallbackQuery):
    if callback_query.data == 'nothing':
        pass
    # elif callback_query.data == 'Отправить сообщения':
    #     user = callback_query.data.lstrip('message:')
    #     await FSM
    else:
        data = callback_query.data
        ban(data.lstrip('ban data:'))
        await bot.send_message(callback_query.message.chat.id, 'Пользователь заблокирован !')
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


def register_admin_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(ban_user, lambda callback_query: filters.Regexp(regexp='^.+'))
