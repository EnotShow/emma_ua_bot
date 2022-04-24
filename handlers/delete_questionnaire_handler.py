from keyboards import recovery_questionnaire_keyboard
from states import FSMDelete, FSMEdit
from bot_create import bot
from database import delete_questionnaire

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext


async def delete_user_questionnaire(message: types.Message, state: FSMContext):
    if message.text == 'Так':
        delete_questionnaire(message.from_user.id)
        await state.finish()
        await FSMDelete.recover.set()
        await bot.send_message(message.from_user.id, 'Анкета видалена! Сподіваюсь ми вам допомогли.'
                                                     ' Ви можете відновити свою анкету у будь-який час.',
                               reply_markup=recovery_questionnaire_keyboard)

    elif message.text == 'Ні':
        await state.finish()
        await FSMDelete.recover.set()
        await bot.send_message(
            message.from_user.id,
            'Ми будемо вас чекати',
            reply_markup=recovery_questionnaire_keyboard
        )


async def recover(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMEdit.age.set()
    await bot.send_message(message.from_user.id, 'Cкільки тобі років?', reply_markup=ReplyKeyboardRemove())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_user_questionnaire, state=FSMDelete.status)
    dp.register_message_handler(recover, state=FSMDelete.recover)
