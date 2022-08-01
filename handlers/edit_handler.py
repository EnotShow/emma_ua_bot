from aiogram.types import ContentType
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.orm import Session

from admin.config import banned_countries
from bot_create import bot
from database import edit_questionnaire, user_questionnaire_template, get_user_questionnaire, \
    register_questionnaire
from database.database import engine
from handlers.welcome_handlers import send_welcome
from keyboards.countries_keyboards import return_city_list, country_buttons
from language.ua.keyboards import *
from language.ua.text import *
from states import FSMEdit, FSMRegister, FSMPhotoEdit, FSMAboutEdit


class QuestionnaireRegister:
    """
    Отвечает за регистрацию анкеты пользователя
    """
    def __init__(self, FSM):
        self.FSM = FSM

    """Получает данные о возрасте пользователя"""
    async def get_age(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            try:
                async with state.proxy() as data:
                    message.text = int(message.text)
                    data['age'] = int(message.text)
                await self.FSM.next()
                await bot.send_message(message.from_user.id, f'{tedit1}', reply_markup=sexb1)
            except:
                await bot.send_message(message.from_user.id, f'{tedit2}')

    """Получает стать пользователя"""

    async def get_sex(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            async with state.proxy() as data:
                if message.text == mb1.text:
                    result = 1
                if message.text == fb1.text:
                    result = 2
                data['sex'] = result
                await self.FSM.next()
                await bot.send_message(message.from_user.id, f'{tedit3}',
                                       reply_markup=ReplyKeyboardRemove())

    """Получает имя пользователя"""

    async def get_name(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            async with state.proxy() as data:
                data['name'] = message.text
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit14}', reply_markup=country_buttons)

    """Получает страну пользователя"""

    async def get_country(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            if message.text.upper() in banned_countries:
                await bot.send_message(message.from_user.id, tedit6, reply_markup=ReplyKeyboardRemove())
            async with state.proxy() as data:
                data['country'] = message.text
            await self.FSM.next()
            city_list = return_city_list(message.text)
            if city_list:
                city_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
                for i in city_list:
                    city_buttons.insert(KeyboardButton(i))
                await bot.send_message(message.from_user.id, f'{tedit4}', reply_markup=city_buttons)
            else:
                await bot.send_message(message.from_user.id, f'{tedit4}', reply_markup=ReplyKeyboardRemove())

    """Получает город пользователя"""

    async def get_city(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            async with state.proxy() as data:
                data['city'] = message.text
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit5}', reply_markup=sexb2)

    """Получает пол пользователей, которых хочет искать пользователь"""

    async def get_find(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            async with state.proxy() as data:
                if message.text == mb2.text:
                    result = 1
                if message.text == fb2.text:
                    result = 2
                data['find'] = result
                await self.FSM.next()
                await bot.send_message(
                    message.from_user.id,
                    f'{tedit7}',
                    reply_markup=ReplyKeyboardRemove()
                )

    """Получает данные о поле 'О себе'"""

    async def get_about(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            async with state.proxy() as data:
                data['about'] = message.text
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit8}')

    """Получает фото пользователя и сохраняет все полученные данные в базу данных"""

    async def get_photo(self, message: types.Message, state: FSMContext):
        if message.content_type == ContentType.TEXT:
            if message.text == '/start':
                await state.finish()
                await send_welcome(message)
            else:
                await bot.send_message(message.from_user.id, f'{tedit8}')
        if message.content_type == ContentType.PHOTO:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
                register_questionnaire(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                    name=data['name'],
                    country=data['country'],
                    age=data['age'],
                    photo_id=data['photo'],
                    about=user_questionnaire_template(data["age"], data["name"], data['country'], data["city"], data["about"]),
                    sex_id=data['sex'],
                    city=data['city'],
                    find_id=data['find']
                )
                await bot.send_photo(
                    message.from_user.id,
                    data['photo'],
                    caption=f'{tedit9}'
                            f'{user_questionnaire_template(data["age"], data["name"], data["country"], data["city"], data["about"])}',
                    reply_markup=main_manu_buttons)
                await state.finish()


class QuestionnaireEdit(QuestionnaireRegister):
    """Редактирования анкеты пользователя"""

    async def get_photo(self, message: types.Message, state: FSMContext):
        if message.content_type == ContentType.TEXT:
            if message.text == '/start':
                await state.finish()
                await send_welcome(message)
            else:
                await bot.send_message(message.from_user.id, f'{tedit8}')
        if message.content_type == ContentType.PHOTO:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
                edit_questionnaire(
                    user_id=message.from_user.id,
                    username=message.from_user.username,
                    name=data['name'],
                    country=data['country'],
                    age=data['age'],
                    photo_id=data['photo'],
                    about=user_questionnaire_template(data["age"], data["name"], data['country'], data["city"], data["about"]),
                    sex_id=data['sex'],
                    city=data['city'],
                    find_id=data['find']
                )
                await bot.send_photo(
                    message.from_user.id,
                    data['photo'],
                    caption=f'{tedit9}'
                            f'{user_questionnaire_template(data["age"], data["name"], data["country"], data["city"], data["about"])}',
                    reply_markup=main_manu_buttons)
                await state.finish()


user_register = QuestionnaireRegister(FSM=FSMRegister)
user_edit = QuestionnaireEdit(FSM=FSMEdit)


async def photo_edit(message: types.Message, state: FSMContext):
    """Отвечает за изменение фото в анкете пользователя"""
    if message.content_type == ContentType.TEXT:
        if message.text == '/start':
            await state.finish()
            await send_welcome(message)
        else:
            await bot.send_message(message.from_user.id, f'{tedit8}')
    if message.content_type == ContentType.PHOTO:
        questionnaire = get_user_questionnaire(message.from_user.id)
        with Session(engine) as session:
            questionnaire.photo = message.photo[0].file_id
            session.add(questionnaire)
            session.commit()
        await state.finish()
        questionnaire = get_user_questionnaire(message.from_user.id)
        await bot.send_photo(
            message.from_user.id,
            questionnaire.photo,
            caption=f'{tedit9}'
                    f'{user_questionnaire_template(questionnaire.age, questionnaire.name, questionnaire.country, questionnaire.city, questionnaire.about)}',
            reply_markup=main_manu_buttons)
        await state.finish()


async def about_edit(message: types.Message, state: FSMContext):
    """Отвечает за изменение информации о пользователи в анкете"""
    if message.text == '/start':
        await state.finish()
        await send_welcome(message)
    else:
        questionnaire = get_user_questionnaire(message.from_user.id)
        with Session(engine) as session:
            questionnaire.about = user_questionnaire_template(
                questionnaire.age,
                questionnaire.name,
                questionnaire.country,
                questionnaire.city,
                message.text
            )
            session.add(questionnaire)
            session.commit()
        await state.finish()
        questionnaire = get_user_questionnaire(message.from_user.id)
        await bot.send_photo(
            message.from_user.id,
            questionnaire.photo,
            caption=f'{tedit9}'
                    f'{user_questionnaire_template(questionnaire.age, questionnaire.name, questionnaire.country, questionnaire.city, questionnaire.about)}',
            reply_markup=main_manu_buttons)
        await state.finish()


def register_user_handlers(dp: Dispatcher):
    # User register
    dp.register_message_handler(user_register.get_age, state=FSMRegister.age)
    dp.register_message_handler(user_register.get_sex, state=FSMRegister.sex)
    dp.register_message_handler(user_register.get_name, state=FSMRegister.name)
    dp.register_message_handler(user_register.get_country, state=FSMRegister.country)
    dp.register_message_handler(user_register.get_city, state=FSMRegister.city)
    dp.register_message_handler(user_register.get_find, state=FSMRegister.find)
    dp.register_message_handler(user_register.get_about, state=FSMRegister.about)
    dp.register_message_handler(user_register.get_photo, state=FSMRegister.photo, content_types=['photo', 'text'])

    # User edit
    dp.register_message_handler(user_edit.get_age, state=FSMEdit.age)
    dp.register_message_handler(user_edit.get_sex, state=FSMEdit.sex)
    dp.register_message_handler(user_edit.get_name, state=FSMEdit.name)
    dp.register_message_handler(user_edit.get_country, state=FSMEdit.country)
    dp.register_message_handler(user_edit.get_city, state=FSMEdit.city)
    dp.register_message_handler(user_edit.get_find, state=FSMEdit.find)
    dp.register_message_handler(user_edit.get_about, state=FSMEdit.about)
    dp.register_message_handler(user_edit.get_photo, state=FSMEdit.photo, content_types=['photo', 'text'])

    # Select edit
    dp.register_message_handler(photo_edit, state=FSMPhotoEdit, content_types=['photo', 'text'])
    dp.register_message_handler(about_edit, state=FSMAboutEdit.about)
