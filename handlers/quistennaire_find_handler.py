import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import random

from bot_create import bot
from database import get_related_users, add_to_like_list, send_report, is_liked, return_to_main_manu
from handlers.main_handlers import send_welcome
from language.ua.text import *
from language.ua.keyboards import *
from states import FSMFind


async def next_find_questionnaire(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        async with state.proxy() as data:
            if message.text == like.text:
                if is_liked(message.from_user.id, data['user']):
                    await bot.send_message(message.from_user.id, f'{tfind1}')
                else:
                    try:
                        add_to_like_list(message.from_user.id, message.from_user.username, data['user'])
                        await bot.send_message(data['user'], f'{tfind2}')
                    except:
                        await bot.send_message(message.from_user.id, f'{tfind6}')

                related_users = data['userlist']
                if len(related_users) == 1:
                    related_users = related_users[0]
                    user_questionnaire = related_users
                    data['userlist'] = get_related_users(message.from_user.id, region_key=False)
                else:
                    user_questionnaire = random.choice(related_users)
                    related_users.remove(user_questionnaire)
                    data['userlist'] = related_users
                data['user'] = user_questionnaire.user_id
                await bot.send_photo(
                    message.chat.id,
                    user_questionnaire.photo,
                    caption=f'''{user_questionnaire.about}''',
                    reply_markup=fbuttons)

            if message.text == like_with_message.text:
                if is_liked(message.from_user.id, data['user']):
                    await bot.send_message(message.from_user.id, f'{tfind1}')
                else:
                    await FSMFind.next()
                    await bot.send_message(
                        message.from_user.id,
                        f'{tfind3}',
                        reply_markup=ReplyKeyboardRemove()
                    )

            if message.text == dislike.text:
                related_users = data['userlist']
                if len(related_users) == 1:
                    related_users = related_users[0]
                    user_questionnaire = related_users
                    data['userlist'] = get_related_users(message.from_user.id, region_key=False)
                else:
                    user_questionnaire = random.choice(related_users)
                    related_users.remove(user_questionnaire)
                    data['userlist'] = related_users
                data['user'] = user_questionnaire.user_id
                await bot.send_photo(
                    message.chat.id,
                    user_questionnaire.photo,
                    caption=f'''{user_questionnaire.about}''',
                    reply_markup=fbuttons)

            if message.text == complain.text:
                await bot.send_message(message.from_user.id, f'{tfind4}')
                related_users = data['userlist']
                if len(related_users) == 1:
                    related_users = related_users[0]
                    user_questionnaire = related_users
                    data['userlist'] = get_related_users(message.from_user.id, region_key=False)
                else:
                    user_questionnaire = random.choice(related_users)
                    related_users.remove(user_questionnaire)
                    data['userlist'] = related_users
                await send_report(data["user"], message.from_user.username)
                data['user'] = user_questionnaire.user_id
                await bot.send_photo(
                    message.chat.id,
                    user_questionnaire.photo,
                    caption=f'''{user_questionnaire.about}''',
                    reply_markup=fbuttons)

            if message.text == exit_query.text:
                await state.finish()
                await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)


async def get_message(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        async with state.proxy() as data:
            data['message'] = message.text
            try:
                add_to_like_list(message.from_user.id, message.from_user.username, data['user'], data['message'])
                await bot.send_message(data['user'], f'{tfind2}')
                await bot.send_message(message.from_user.id, f'{tfind7}')
            except:
                await bot.send_message(
                    message.from_user.id,
                    f'{tfind6}'
                )
        await state.finish()
        await FSMFind.user.set()
        related_users = data['userlist']
        if len(related_users) == 1:
            related_users = related_users[0]
            user_questionnaire = related_users
            data['userlist'] = get_related_users(message.from_user.id, region_key=False)
        else:
            user_questionnaire = random.choice(related_users)
            related_users.remove(user_questionnaire)
        async with state.proxy() as data:
            data['userlist'] = related_users
            data['user'] = user_questionnaire.user_id
        await bot.send_photo(
            message.chat.id,
            user_questionnaire.photo,
            caption=f'''{user_questionnaire.about}''',
            reply_markup=fbuttons)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(next_find_questionnaire, state=FSMFind.user)
    dp.register_message_handler(get_message, state=FSMFind.message)
