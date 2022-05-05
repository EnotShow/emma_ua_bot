import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.database import engine, Questionnaire, Likes, DBSession
from language.ua import city_list

from bot_create import bot

from admin import admin_chat_id


def get_user_questionnaire(user_id):
    with Session(engine) as session:
        stmt = select(Questionnaire).where(Questionnaire.user_id == user_id)
        questionnaire = session.scalars(stmt).one()
    return questionnaire


def register_questionnaire(user_id, username, name, age, photo_id, about, sex_id, city, find_id):
    with Session(engine) as session:
        user_questionnaire = Questionnaire(
            user_id=user_id,
            username=username,
            name=name,
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


def edit_questionnaire(user_id, username, name, age, photo_id, about, sex_id, city, find_id):
    with Session(engine) as session:
        questionnaire = get_user_questionnaire(user_id)
        if questionnaire:
            questionnaire.username = username
            questionnaire.photo = photo_id
            questionnaire.about = about
            questionnaire.name = name
            questionnaire.age = age
            questionnaire.sex = sex_id
            questionnaire.city = city
            questionnaire.find = find_id
            questionnaire.is_delete = False
        session.add(questionnaire)
        session.commit()


def get_related_users(user_id, region_key=True):
    with Session(engine) as session:
        questionnaire = get_user_questionnaire(user_id)
        city = questionnaire.city
        to_find = questionnaire.find
        if region_key:
            stmt = select(Questionnaire).where(
                Questionnaire.user_id != user_id,
                Questionnaire.sex == to_find,
                Questionnaire.city == city,
                Questionnaire.is_delete == False,
                Questionnaire.is_banned == False
            )
        else:
            stmt = select(Questionnaire).where(
                Questionnaire.user_id != user_id,
                Questionnaire.sex == to_find,
                Questionnaire.city != city,
                Questionnaire.is_delete == False,
                Questionnaire.is_banned == False
            )

        related_users = engine.connect().execute(stmt).fetchall()
        if related_users:
            return related_users


def add_to_like_list(user_id, username, related_user_id, message=False):
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
    stmt = select(Questionnaire.user_id, Questionnaire.is_delete).where(Questionnaire.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result:
        return result
    else:
        return False


def give_user_who_like(current_user_id):
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
    session = DBSession()
    user = get_user_questionnaire(user_id)
    user.is_delete = False
    session.add(user)
    session.commit()


def is_liked(user_id, related_user_id):
    stmt = select(Likes).where(Likes.questionnaire_user_id == related_user_id, Likes.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result:
        return True
    else:
        return False


def is_banned(user_id):
    stmt = select(Questionnaire.is_banned).where(Questionnaire.user_id == user_id)
    result = engine.connect().execute(stmt).fetchone()
    if result.is_banned:
        return True
    else:
        return False


async def send_report(reported_user_id, reporter_username):
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
    questionnaire = get_user_questionnaire(user)
    if questionnaire.username != str('None'):
        return True


def return_to_main_manu(message_text):
    if message_text == '/main_manu':
        return True


def city_filter(message_text):
    for i in city_list:
        if i == message_text:
            return True


# async def _user_selector_algorith(user_id, method, state):
#     async with state.proxy as data:
#         related_users = method
#         if len(related_users) == 1:
#             related_users = related_users[0]
#             user_questionnaire = related_users
#             data['userlist'] = get_related_users(user_id, region_key=False)
#         else:
#             user_questionnaire = random.choice(related_users)
#             data['userlist'] = related_users.remove(user_questionnaire)
#         data['user'] = user_questionnaire.user_id
#         return user_questionnaire
