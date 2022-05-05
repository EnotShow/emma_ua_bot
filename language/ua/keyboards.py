from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainb = KeyboardButton('Головне меню')
# main manu buttons
b1 = KeyboardButton('Знайомитись ☘️')
b2 = KeyboardButton('Кому я сподобався')
b3 = KeyboardButton('Моя анкета')

main_manu_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
main_manu_buttons.add(b1).insert(b2).add(b3)

# register/edit buttons

mb1 = KeyboardButton('Хлопець')
fb1 = KeyboardButton('Дівчина')

sexb1 = ReplyKeyboardMarkup(resize_keyboard=True)
sexb1.add(mb1).insert(fb1)

mb2 = KeyboardButton('Хлопці')
fb2 = KeyboardButton('Дівчата')

sexb2 = ReplyKeyboardMarkup(resize_keyboard=True)
sexb2.add(mb2).insert(fb2)

editb1 = KeyboardButton('Переглянути мою анкету')
editb2 = KeyboardButton('Редагувати мою анкету')
b4 = KeyboardButton('Видалити мою анкету')

editk1 = ReplyKeyboardMarkup(resize_keyboard=True)
editk1.add(editb1).insert(editb2).add(b4).add(mainb)

editb3 = KeyboardButton('Заповнити анкету заново')
editb4 = KeyboardButton('Змінити фото')
editb5 = KeyboardButton('Змінити "Про себе"')
editb6 = KeyboardButton('Я змінив нікнейм')

editk2 = ReplyKeyboardMarkup(resize_keyboard=True)
editk2.add(editb3).add(editb4).insert(editb5).add(editb6).add(mainb)

# city select buttons

city1 = KeyboardButton('Варшава')
city2 = KeyboardButton('Краків')
city3 = KeyboardButton('Лодзь')
city4 = KeyboardButton('Вроцлав')
city5 = KeyboardButton('Познань')
city6 = KeyboardButton('Гданьськ')
city7 = KeyboardButton('Щецин')
city8 = KeyboardButton('Бидгощ')
city9 = KeyboardButton('Люблин')
city10 = KeyboardButton('Катовіце')
city_list = ['Варшава', 'Краків', 'Лодзь', 'Вроцлав', 'Познань', 'Гданьськ', 'Щецин', 'Бидгощ', 'Люблин', 'Катовіце']

cityb = ReplyKeyboardMarkup(resize_keyboard=True)
cityb.add(city1).row(city2, city3, city4).row(city5, city6, city7).row(city8, city9, city10)

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

recoverb = KeyboardButton('Відновити анкету')
recovery_questionnaire_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(recoverb)
