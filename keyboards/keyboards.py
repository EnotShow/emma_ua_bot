from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# main manu buttons
b1 = KeyboardButton('Знайомитись ☘️')
b2 = KeyboardButton('Кому я сподобався')
b3 = KeyboardButton('Редагувати мою анкету')
b4 = KeyboardButton('Видалити мою анкету')

main_manu_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
main_manu_buttons.add(b1).insert(b2).add(b3).insert(b4)

# register/edit buttons

mb1 = KeyboardButton('Хлопець')
fb1 = KeyboardButton('Дівчина')

sexb1 = ReplyKeyboardMarkup(resize_keyboard=True)
sexb1.add(mb1).insert(fb1)

mb2 = KeyboardButton('Хлопці')
fb2 = KeyboardButton('Дівчата')

sexb2 = ReplyKeyboardMarkup(resize_keyboard=True)
sexb2.add(mb2).insert(fb2)

# select questionnaire buttons

like = KeyboardButton('💙')
dislike = KeyboardButton('❌')
like_with_message = KeyboardButton('💬')
complain = KeyboardButton('Поскаржитися')
exit_query = KeyboardButton('Я втомився')

fbuttons = ReplyKeyboardMarkup(resize_keyboard=True)
fbuttons.add(like).insert(like_with_message).insert(dislike).add(complain).add(exit_query)

wlbutton = ReplyKeyboardMarkup(resize_keyboard=True)
wlbutton.add(like).insert(dislike).add(exit_query)

allow_button = KeyboardButton('Так')
cancel_button = KeyboardButton('Ні')

confirmation_button = ReplyKeyboardMarkup(resize_keyboard=True)
confirmation_button.add(allow_button).insert(cancel_button)

recovery_questionnaire_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Відновити анкету'))
