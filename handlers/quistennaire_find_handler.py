import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import random

from bot_create import bot
from database import get_related_users, add_to_like_list, send_report, is_liked
from handlers.main_handlers import send_welcome
from language.ua.text import *
from language.ua.keyboards import *
from states import FSMFind


async def next_find_questionnaire(message: types.Message, state: FSMContext):
    """
    Получает случайную анкету из списка подходящих анкет
    """
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        if message.text == exit_query.text:
            await state.finish()
            await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)
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
                    pass

                if message.text == complain.text:
                    await bot.send_message(message.from_user.id, f'{tfind4}')
                    async with state.proxy() as data:
                        await send_report(data["user"], message.from_user.username)

                try:
                    related_users = data['userlist']
                    if related_users:
                        if len(related_users) == 1:
                            related_users = related_users[0]
                            user_questionnaire = related_users
                            try:
                                data['userlist'] = get_related_users(message.from_user.id, region_key=False)
                            except:
                                data['userlist'] = False
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
                    else:
                        await state.finish()
                        await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)
                except:
                    await state.finish()
                    await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)


async def get_message(message: types.Message, state: FSMContext):
    """
    Получает сообщение от пользователя, которое нужно доставить понравившемуся пользователю
    """
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
        try:
            related_users = data['userlist']
            if related_users:
                if len(related_users) == 1:
                    related_users = related_users[0]
                    user_questionnaire = related_users
                    try:
                        data['userlist'] = get_related_users(message.from_user.id, region_key=False)
                    except:
                        data['userlist'] = False
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
            else:
                await state.finish()
                await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)
        except:
            await state.finish()
            await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(next_find_questionnaire, state=FSMFind.user)
    dp.register_message_handler(get_message, state=FSMFind.message)
