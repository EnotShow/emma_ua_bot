from sqlalchemy.orm import Session

from bot_create import bot
from database import edit_questionnaire, user_questionnaire_template, city_filter, get_user_questionnaire, \
    register_questionnaire
from database.database import engine
from language.ua import sexb1, sexb2, cityb, main_manu_buttons
from language.ua.keyboards import *
from language.ua.text import *
from states import FSMEdit, FSMMenu, FSMRegister, FSMPreEdit, FSMPhotoEdit, FSMAboutEdit, FSMUsernameEdit

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


class QuestionnaireRegister:

    def __init__(self, FSM):
        self.FSM = FSM

    async def get_age(self, message: types.Message, state: FSMContext):
        try:
            async with state.proxy() as data:
                message.text = int(message.text)
                data['age'] = int(message.text)
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit1}', reply_markup=sexb1)
        except:
            await bot.send_message(message.from_user.id, f'{tedit2}')

    async def get_sex(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if message.text == mb1.text:
                result = 1
            if message.text == fb1.text:
                result = 2
            data['sex'] = result
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit3}',
                                   reply_markup=ReplyKeyboardRemove())

    async def get_name(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        await self.FSM.next()
        await bot.send_message(message.from_user.id, f'{tedit4}', reply_markup=cityb)

    async def get_city(self, message: types.Message, state: FSMContext):
        if city_filter(message.text):
            async with state.proxy() as data:
                data['city'] = message.text
            await self.FSM.next()
            await bot.send_message(message.from_user.id, f'{tedit5}', reply_markup=sexb2)
        else:
            await bot.send_message(message.from_user.id, f'{tedit6}')

    async def get_find(self, message: types.Message, state: FSMContext):
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

    async def get_about(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['about'] = message.text
        await self.FSM.next()
        await bot.send_message(message.from_user.id, f'{tedit8}')

    async def get_photo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            register_questionnaire(
                user_id=message.from_user.id,
                username=message.from_user.username,
                name=data['name'],
                age=data['age'],
                photo_id=data['photo'],
                about=user_questionnaire_template(data["age"], data["name"], data["city"], data["about"]),
                sex_id=data['sex'],
                city=data['city'],
                find_id=data['find']
            )
            await bot.send_photo(
                message.from_user.id,
                data['photo'],
                caption=f'{tedit9}'
                        f'{user_questionnaire_template(data["age"], data["name"], data["city"], data["about"])}',
                reply_markup=main_manu_buttons)

            await FSMRegister.next()
            await state.finish()
            await FSMMenu.status.set()


class QuestionnaireEdit(QuestionnaireRegister):

    async def get_photo(self, message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            edit_questionnaire(
                user_id=message.from_user.id,
                username=message.from_user.username,
                name=data['name'],
                age=data['age'],
                photo_id=data['photo'],
                about=user_questionnaire_template(data["age"], data["name"], data["city"], data["about"]),
                sex_id=data['sex'],
                city=data['city'],
                find_id=data['find']
            )
            await bot.send_photo(
                message.from_user.id,
                data['photo'],
                caption=f'{tedit9}'
                        f'{user_questionnaire_template(data["age"], data["name"], data["city"], data["about"])}',
                reply_markup=main_manu_buttons)
            await self.FSM.next()
            await state.finish()
            await FSMMenu.status.set()


user_register = QuestionnaireRegister(FSM=FSMRegister)
user_edit = QuestionnaireEdit(FSM=FSMEdit)


async def edit_selector(message: types.Message, state: FSMContext):
    if message.text == editb1.text:
        await state.finish()
        await FSMMenu.status.set()
        questionnaire = get_user_questionnaire(message.from_user.id)
        await bot.send_photo(
            message.from_user.id,
            questionnaire.photo,
            caption=f'{questionnaire.about}',
            reply_markup=main_manu_buttons
        )
    elif message.text == editb2.text:
        await FSMPreEdit.next()
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=editk2)
    elif message.text == mainb.text:
        await FSMMenu.status.set()
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)


async def edit_selector_two(message: types.Message, state: FSMContext):
    await state.finish()
    if message.text == editb3.text:
        print('it work')
        await FSMEdit.age.set()
        await bot.send_message(message.from_user.id, f'{tmain4}')
    elif message.text == editb4.text:
        await FSMPhotoEdit.photo.set()
        await bot.send_message(message.from_user.id, f'{tedit10}')
    elif message.text == editb5.text:
        await FSMAboutEdit.about.set()
        await bot.send_message(message.from_user.id, f'{tedit11}')
    elif message.text == editb6.text:
        await state.finish()
        await FSMMenu.status.set()
        questionnaire = get_user_questionnaire(message.from_user.id)
        with Session(engine) as session:
            questionnaire.username = message.from_user.username
            session.add(questionnaire)
            session.commit()
        await bot.send_message(message.from_user.id, f'{tedit12}', reply_markup=main_manu_buttons)
    elif message.text == mainb.text:
        await FSMMenu.status.set()
        await bot.send_message(message.from_user.id, f'{tfind5}', reply_markup=main_manu_buttons)


async def photo_edit(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMMenu.status.set()
    questionnaire = get_user_questionnaire(message.from_user.id)
    with Session(engine) as session:
        questionnaire.photo = message.photo[0].file_id
        session.add(questionnaire)
        session.commit()
    await bot.send_message(message.from_user.id, f'{tedit13}', reply_markup=main_manu_buttons)


async def about_edit(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMMenu.status.set()
    questionnaire = get_user_questionnaire(message.from_user.id)
    with Session(engine) as session:
        questionnaire.about = user_questionnaire_template(
            questionnaire.age,
            questionnaire.name,
            questionnaire.city,
            message.text
        )
        session.add(questionnaire)
        session.commit()
    await bot.send_message(message.from_user.id, f'{tedit14}', reply_markup=main_manu_buttons)


def register_user_handlers(dp: Dispatcher):
    # User register
    dp.register_message_handler(user_register.get_age, state=FSMRegister.age)
    dp.register_message_handler(user_register.get_sex, state=FSMRegister.sex)
    dp.register_message_handler(user_register.get_name, state=FSMRegister.name)
    dp.register_message_handler(user_register.get_city, state=FSMRegister.city)
    dp.register_message_handler(user_register.get_find, state=FSMRegister.find)
    dp.register_message_handler(user_register.get_about, state=FSMRegister.about)
    dp.register_message_handler(user_register.get_photo, content_types=['photo'], state=FSMRegister.photo)

    # User edit
    dp.register_message_handler(user_edit.get_age, state=FSMEdit.age)
    dp.register_message_handler(user_edit.get_sex, state=FSMEdit.sex)
    dp.register_message_handler(user_edit.get_name, state=FSMEdit.name)
    dp.register_message_handler(user_edit.get_city, state=FSMEdit.city)
    dp.register_message_handler(user_edit.get_find, state=FSMEdit.find)
    dp.register_message_handler(user_edit.get_about, state=FSMEdit.about)
    dp.register_message_handler(user_edit.get_photo, content_types=['photo'], state=FSMEdit.photo)

    # Select edit
    dp.register_message_handler(edit_selector, state=FSMPreEdit.state_one)
    dp.register_message_handler(edit_selector_two, state=FSMPreEdit.state_two)
    dp.register_message_handler(photo_edit, content_types=['photo'], state=FSMPhotoEdit.photo)
    dp.register_message_handler(about_edit, state=FSMAboutEdit.about)
