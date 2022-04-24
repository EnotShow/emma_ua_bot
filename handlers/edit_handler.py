from bot_create import bot
from database import edit_questionnaire, user_questionnaire_template, city_filter
from keyboards import sexb1, sexb2, cityb, main_manu_buttons
from states import FSMEdit, FSMMenu

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove


async def get_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            message.text = int(message.text)
            data['age'] = int(message.text)
        await FSMEdit.next()
        await bot.send_message(message.from_user.id, 'Хто ти?', reply_markup=sexb1)
    except:
        await bot.send_message(message.from_user.id, 'Вік повинен бути вказаний числом')


async def get_sex(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Хлопець':
            result = 1
            data['sex'] = result
            await FSMEdit.next()
            await bot.send_message(message.from_user.id, 'Як тебе можна називати?', reply_markup=ReplyKeyboardRemove())

        if message.text == 'Дівчина':
            result = 2
            data['sex'] = result
            await FSMEdit.next()
            await bot.send_message(message.from_user.id, 'Як тебе можна називати?', reply_markup=ReplyKeyboardRemove())


async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMEdit.next()
    await bot.send_message(message.from_user.id, 'Звідки ти?', reply_markup=cityb)


# TODO city filter
async def get_city(message: types.Message, state: FSMContext):
    if city_filter(message.text):
        async with state.proxy() as data:
            data['city'] = message.text
        await FSMEdit.next()
        await bot.send_message(message.from_user.id, 'Хто тебе цікавить?🤓', reply_markup=sexb2)
    else:
        await bot.send_message(message.from_user.id, 'Вибери місто із списку')


async def get_find(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Хлопці':
            result = 1
            data['find'] = result
            await FSMEdit.next()
            await bot.send_message(
                message.from_user.id,
                'Роскажи щось про себе. Що ти тут шукаєш?',
                reply_markup=ReplyKeyboardRemove()
            )
        if message.text == 'Дівчата':
            result = 2
            data['find'] = result
            await FSMEdit.next()
            await bot.send_message(
                message.from_user.id,
                'Роскажи щось про себе. Що ти тут шукаєш?',
                reply_markup=ReplyKeyboardRemove()
            )


async def get_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
    await FSMEdit.next()
    await bot.send_message(message.from_user.id, 'Відправ фото яке хочеш представити у своїй анкеті')


async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        edit_questionnaire(
            user_id=message.from_user.id,
            username=message.from_user.username,
            photo_id=data['photo'],
            about=user_questionnaire_template(data["age"], data["name"], data["city"], data["about"]),
            sex_id=data['sex'],
            city=data['city'],
            find_id=data['find']
        )
        await bot.send_photo(
            message.from_user.id,
            data['photo'],
            caption=f'Ось твоя анкета:\n\n'
                    f'{user_questionnaire_template(data["age"], data["name"], data["city"], data["about"])}',
            reply_markup=main_manu_buttons)

        await FSMEdit.next()
        await state.finish()
        await FSMMenu.status.set()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(get_age, state=FSMEdit.age)
    dp.register_message_handler(get_sex, state=FSMEdit.sex)
    dp.register_message_handler(get_name, state=FSMEdit.name)
    dp.register_message_handler(get_city, state=FSMEdit.city)
    dp.register_message_handler(get_find, state=FSMEdit.find)
    dp.register_message_handler(get_about, state=FSMEdit.about)
    dp.register_message_handler(get_photo, content_types=['photo'], state=FSMEdit.photo)
