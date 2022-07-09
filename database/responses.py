import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.database import engine, Questionnaire, Likes, DBSession
from language.ua import city_list

from bot_create import bot

from admin import admin_chat_id


def get_user_questionnaire(user_id):
    """
    Получает анкету пользователя из базы данных
    """
    with Session(engine) as session:
        stmt = select(Questionnaire).where(Questionnaire.user_id == user_id)
        questionnaire = session.scalars(stmt).one()
    return questionnaire


def register_questionnaire(user_id, username, name, country, age, photo_id, about, sex_id, city, find_id):
    """
    Отвечает за добавление анкеты пользователя в базу данных
    """
    with Session(engine) as session:
        user_questionnaire = Questionnaire(
            user_id=user_id,
            username=username,
            name=name,
            country=country,
            age=age,
            photo=photo_id,
            about=about,
            sex=sex_id,
            city=city,
            find=find_id,
            is_delete=False
        )

    session.add(user_questionnaire)
    session.commit()


def edit_questionnaire(user_id, username, name, country, age, photo_id, about, sex_id, city, find_id):
    """
    Отвечает за редактирование уже существующей анкеты
    """
    with Session(engine) as session:
        questionnaire = get_user_questionnaire(user_id)
        if questionnaire:
            questionnaire.username = username
            questionnaire.photo = photo_id
            questionnaire.about = about
            questionnaire.name = name
            questionnaire.country = country
            questionnaire.age = age
            questionnaire.sex = sex_id
            questionnaire.city = city
            questionnaire.find = find_id
            questionnaire.is_delete = False
        session.add(questionnaire)
        session.commit()


def get_related_users(user_id, region_key=True, country_key=True):
    """
    Получает список анкет для выдачи
    """
    questionnaire = get_user_questionnaire(user_id)
    country = questionnaire.country
    city = questionnaire.city
    to_find = questionnaire.find
    if region_key:
        stmt = select(Questionnaire).where(
            Questionnaire.user_id != user_id,
            Questionnaire.sex == to_find,
            Questionnaire.city == city,
            Questionnaire.country == country,
            Questionnaire.is_delete == False,
            Questionnaire.is_banned == False
        )
    elif not region_key and not country_key:
        stmt = select(Questionnaire).where(
            Questionnaire.user_id != user_id,
            Questionnaire.sex == to_find,
            Questionnaire.country != country,
            Questionnaire.is_delete == False,
            Questionnaire.is_banned == False
        )
    else:
        stmt = select(Questionnaire).where(
            Questionnaire.user_id != user_id,
            Questionnaire.sex == to_find,
            Questionnaire.country == country,
            Questionnaire.city != city,
            Questionnaire.is_delete == False,
            Questionnaire.is_banned == False
        )

    related_users = engine.connect().execute(stmt).fetchall()
    if related_users:
        return related_users


def add_to_like_list(user_id, username, related_user_id, message=False):
    """
    Добавляет анкету, которая понравилась пользователю в таблицу Likes
    """
    with Session(engine) as session:
        if message:
            likes = Likes(
                user_id=user_id,
                username=username,
                questionnaire_user_id=related_user_id,
                message=message,
            )
        else:
            likes = Likes(
                user_id=user_id,
                username=username,
                questionnaire_user_id=related_user_id,
            )

    session.add(likes)
    session.commit()


def is_registered(user_id):
    """
    Проверяет есть ли запись пользователя в базе данных
    """
    stmt = select(Questionnaire.user_id, Questionnaire.is_delete).where(Questionnaire.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result:
        return result
    else:
        return False


def give_user_who_like(current_user_id):
    """
    Получает из баззы данных список анкет пользователей, которые поставили лайк
    """
    stmt = select([Likes.user_id, Likes.message]).where(Likes.questionnaire_user_id == current_user_id)
    related_user = engine.connect().execute(stmt).fetchone()
    if str(related_user) != 'None':
        stmt = select(Questionnaire).where(Questionnaire.user_id == related_user.user_id)
        user_questionnaire = engine.connect().execute(stmt).fetchone()
        session = DBSession()
        x = session.query(Likes).filter(Likes.questionnaire_user_id == current_user_id).first()
        session.delete(x)
        session.commit()
        return user_questionnaire, related_user.message
    else:
        return False


def delete_questionnaire(user_id):
    """
    Устанавливает флаг is_delete == True для текущего пользователя
    """
    session = DBSession()
    user = get_user_questionnaire(user_id)
    user.is_delete = True
    try:
        session.query(Likes).filter(Likes.questionnaire_user_id == user.user_id).delete(synchronize_session='evaluate')
    except:
        pass
    session.add(user)
    session.commit()


def recover_questionnaire(user_id):
    """
    Устанавливает флаг is_delete == False для текущего пользователя
    """
    session = DBSession()
    user = get_user_questionnaire(user_id)
    user.is_delete = False
    session.add(user)
    session.commit()


def is_liked(user_id, related_user_id):
    """
    Проверяет была ли лайкнута анкета пользователем ранне
    """
    stmt = select(Likes).where(Likes.questionnaire_user_id == related_user_id, Likes.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result:
        return True
    else:
        return False


def is_banned(user_id):
    """
    Проверяет наличия блокировки у пользователя
    """
    stmt = select(Questionnaire.is_banned).where(Questionnaire.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result.is_banned:
        return True
    else:
        return False


async def send_report(reported_user_id, reporter_username):
    """
    Отправляет репорт в админ. чат
    """
    report_reply1 = InlineKeyboardButton('Забанить', callback_data=f'ban data:{reported_user_id}')
    report_reply2 = InlineKeyboardButton('Ничего не делать', callback_data='nothing')
    report_reply3 = InlineKeyboardButton('Отправить сообщния', callback_data=f'message:{reported_user_id}')
    report_keyboard = InlineKeyboardMarkup().add(report_reply1).insert(report_reply2)
    stmt = select(Questionnaire).where(Questionnaire.user_id == reported_user_id)
    result = engine.connect().execute(stmt).fetchone()
    report = f'Получена жалоба от пользователя @{reporter_username}, на:\n{result.about}\n\nЕго id - {result.id};' \
             f'\nЕго user_id - {result.user_id};\nЕго username - @{result.username};'
    await bot.send_photo(admin_chat_id, result.photo, caption=report, reply_markup=report_keyboard)


def check_username(user):
    """
    Проверяет наличия username у пользователя
    """
    questionnaire = get_user_questionnaire(user)
    try:
        if questionnaire.username:
            return True
    except:
        return False


def city_filter(message_text):
    """
    Проверяет есть ли город пользователя в списке поддерживаймых городов
    """
    for i in city_list:
        if i == message_text:
            return True
