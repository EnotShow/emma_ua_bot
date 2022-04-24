from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import random

from bot_create import bot
from database import get_related_users, add_to_like_list, send_report, is_liked
from keyboards import *
from states import FSMFind, FSMMenu


# TODO translate
async def next_find_questionnaire(message: types.Message, state: FSMContext):
    if message.text == '💙':
        async with state.proxy() as data:
            if is_liked(message.from_user.id, data['user']):
                await bot.send_message(message.from_user.id, 'Ви уже відправляли симпатію цьому користувачеві')
            else:
                try:
                    add_to_like_list(message.from_user.id, message.from_user.username, data['user'])
                    await bot.send_message(data['user'], 'Ви комусь сподобалися')
                except:
                    await bot.send_message(
                        message.from_user.id,
                        'Сталася помилка, можливо ви вже відправляли вподобання цьому користувачеві'
                    )
            related_users = get_related_users(message.from_user.id)
            user_questionnaire = random.choice(related_users)
            data['user'] = user_questionnaire.user_id
        await bot.send_photo(
            message.chat.id,
            user_questionnaire.photo,
            caption=f'''{user_questionnaire.about}''',
            reply_markup=fbuttons)

    if message.text == '💬':
        async with state.proxy() as data:
            if is_liked(message.from_user.id, data['user']):
                await bot.send_message(message.from_user.id, 'Ви уже відправляли симпатію цьому користувачеві')
            else:
                await FSMFind.next()
                await bot.send_message(
                    message.from_user.id,
                    'Введіть ваше повідомлення',
                    reply_markup=ReplyKeyboardRemove()
                )

    if message.text == '❌':
        related_users = get_related_users(message.from_user.id)
        user_questionnaire = random.choice(related_users)
        async with state.proxy() as data:
            data['user'] = user_questionnaire.user_id
        await bot.send_photo(
            message.chat.id,
            user_questionnaire.photo,
            caption=f'''{user_questionnaire.about}''',
            reply_markup=fbuttons)

    if message.text == 'Поскаржитися':
        await bot.send_message(message.from_user.id, 'Скарга відправленна')
        related_users = get_related_users(message.from_user.id)
        user_questionnaire = random.choice(related_users)
        async with state.proxy() as data:
            await send_report(data["user"], message.from_user.username)
            data['user'] = user_questionnaire.user_id
        await bot.send_photo(
            message.chat.id,
            user_questionnaire.photo,
            caption=f'''{user_questionnaire.about}''',
            reply_markup=fbuttons)

    if message.text == 'Я втомився':
        await state.finish()
        await FSMMenu.status.set()
        await bot.send_message(message.from_user.id, 'Що далі?', reply_markup=main_manu_buttons)


# TODO delete from the code
async def get_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
        try:
            add_to_like_list(message.from_user.id, message.from_user.username, data['user'], data['message'])
            await bot.send_message(data['user'], "Вы комусь сподобалися")
        except:
            await bot.send_message(
                message.from_user.id,
                'Сталася помилка'
            )
    await state.finish()
    await FSMFind.user.set()
    related_users = get_related_users(message.from_user.id)
    user_questionnaire = random.choice(related_users)
    await bot.send_message(message.from_user.id, 'Повідомлення відправленно !')
    async with state.proxy() as data:
        data['user'] = user_questionnaire.user_id
    await bot.send_photo(
        message.chat.id,
        user_questionnaire.photo,
        caption=f'''{user_questionnaire.about}''',
        reply_markup=fbuttons)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(next_find_questionnaire, state=FSMFind.user)
    dp.register_message_handler(get_message, state=FSMFind.message)
