import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import random

from bot_create import bot
from database import get_related_users, add_to_like_list, send_report, is_liked
from handlers.welcome_handlers import send_welcome
from language.ua.text import *
from language.ua.keyboards import *
from states import FSMFind, FSMFindSwitchToInternational, FSMStartFind


class QuestionnaireFind:

    def __init__(self, international):
        self.international = international

    async def start_find_questionnaire(self, message: types.Message, state: FSMContext):
        await state.finish()
        if self.international:
            await FSMFind.international.set()
        else:
            await FSMFind.not_international.set()
        async with state.proxy() as data:
            if self.international:
                related_users = get_related_users(message.from_user.id, region_key=False, country_key=False)
            else:
                related_users = get_related_users(message.from_user.id)
                if not related_users:
                    related_users = get_related_users(message.from_user.id, region_key=False)
            if related_users:
                if len(related_users) == 1:
                    related_users = related_users[0]
                    user_questionnaire = related_users
                    data['userlist'] = False
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
            elif self.international:
                await state.finish()
                await bot.send_message(message.from_user.id, f'{tmain5}', reply_markup=main_manu_buttons)
            else:
                await state.finish()
                await FSMFindSwitchToInternational.status.set()
                await bot.send_message(message.from_user.id, f'{tmain10}', reply_markup=confirmation_button)

    async def next_find_questionnaire(self, message: types.Message, state: FSMContext):
        """
        Получает случайную анкету из списка подходящих анкет
        """
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        elif message.text == exit_query.text:
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
                    # pass
                    if is_liked(message.from_user.id, data['user']):
                        await bot.send_message(message.from_user.id, f'{tfind1}')
                    else:
                        await FSMFind.next()
                        await bot.send_message(
                            message.from_user.id,
                            f'{tfind3}',
                            reply_markup=ReplyKeyboardRemove()
                        )
                else:
                    if message.text == dislike.text:
                        pass

                    if message.text == complain.text:
                        await bot.send_message(message.from_user.id, f'{tfind4}')
                        async with state.proxy() as data:
                            await send_report(data["user"], message.from_user.username)
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
                        if not self.international:
                            await bot.send_message(message.from_user.id, f'{tmain11}', reply_markup=confirmation_button)
                            await state.finish()
                            await FSMFindSwitchToInternational.status.set()
                        else:
                            await state.finish()
                            await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)

    async def get_message(self, message: types.Message, state: FSMContext):
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
                    if not self.international:
                        await bot.send_message(message.from_user.id, f'{tmain11}', reply_markup=confirmation_button)
                        await state.finish()
                        await FSMFindSwitchToInternational.status.set()
                    else:
                        await state.finish()
                        await bot.send_message(message.from_user.id, f'{tfind8}', reply_markup=main_manu_buttons)


start_not_international_search = QuestionnaireFind(international=False).start_find_questionnaire
start_international_search = QuestionnaireFind(international=True).start_find_questionnaire

next_find_questionnaire_not_international = QuestionnaireFind(international=False).next_find_questionnaire
next_find_questionnaire_international = QuestionnaireFind(international=True).next_find_questionnaire

get_message_not_international = QuestionnaireFind(international=False).get_message
get_message_international = QuestionnaireFind(international=True).get_message


async def select_international_list(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        if message.text == allow_button.text:
            await state.finish()
            await start_international_search(message, state)

        if message.text == cancel_button.text:
            await state.finish()
            await bot.send_message(message.from_user.id, tfind5, reply_markup=main_manu_buttons)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(next_find_questionnaire_not_international, state=FSMFind.not_international)
    dp.register_message_handler(next_find_questionnaire_international, state=FSMFind.international)
    dp.register_message_handler(get_message_not_international, state=FSMFind.message_not_international)
    dp.register_message_handler(get_message_international, state=FSMFind.message_international)
    dp.register_message_handler(select_international_list, state=FSMFindSwitchToInternational.status)
