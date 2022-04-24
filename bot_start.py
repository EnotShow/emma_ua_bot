import logging
import os
from aiogram.utils.executor import start_webhook

from database import create_db
from bot_create import dp, bot, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print('Бот запущен !')
    create_db()
    print('База данных подключена')


async def on_shutdown(_):
    await bot.delete_webhook()
    print('Вебхук удален !')


from handlers import *
from admin import *

main_handlers.register_user_handlers(dp)
user_register_handler.register_user_handlers(dp)
edit_handler.register_user_handlers(dp)
quistennaire_find_handler.register_user_handlers(dp)
watch_like_list.register_user_handlers(dp)
delete_questionnaire_handler.register_user_handlers(dp)

inline_reply_handlers.register_admin_handlers(dp)
admin_features.register_admin_handlers(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
