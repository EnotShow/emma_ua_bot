from aiogram import executor

from database import create_db
from bot_create import dp
from bot_create import bot
from admin import *


async def on_startup(_):
    print('Бот запущен !')
    create_db()
    print('База данных подключена')
    await bot.send_message(admin_chat_id, 'Бот запущен !')


from handlers import *

admin_features.register_admin_handlers(dp)
welcome_handlers.register_user_handlers(dp)
main_manu_handler.register_user_handlers(dp)
edit_handler.register_user_handlers(dp)
quistennaire_find_handler.register_user_handlers(dp)
watch_like_list.register_user_handlers(dp)
delete_questionnaire_handler.register_user_handlers(dp)
inline_reply_handlers.register_admin_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
