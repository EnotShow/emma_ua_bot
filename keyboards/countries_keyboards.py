from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

country_list = ['Україна', 'Польша', 'Чехія', 'Германія', 'Грузія', 'Італия', 'Іспанія', 'Венгрія', 'Молдовія',
                'Словакія', 'Руминія', 'Латвія', 'Португалія', 'Болгарія', 'Фінляндія']

country_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for i in country_list:
    country_buttons.insert(KeyboardButton(i))


def return_city_list(country: str):
    city_list = None
    # if country == 'Україна':
    #     city_list = ["Київ", "Одеса", "Дніпро", "Львів", "Миколаїв", "Севастополь", "Вінниця", "Сімферополь",
    #                  "Херсон", "Сумми", "Черкаси"]

    if country == 'Польша':
        city_list = ['Варшава', 'Краків', 'Лодзь', 'Вроцлав', 'Познань', 'Гданьськ', 'Щецин', 'Бидгощ', 'Люблин',
                     'Катовіце']

    if country == 'Чехія':
        city_list = ["Прага", "Брно", "Острова", "Плезнь", "Ліберець", "Оломоуць", "Усті-над-Лабою",
                     "Чеські Будейовиці", "Градець-Карорве", "Пардубиці"]

    if country == 'Германія':
        city_list = ["Берлін", "Гамбург", "Мюнхен", "Кельн", "Франкфурт", "Штутгарт", "Дюссельдорф", "Лейпциг",
                     "Дортмунд", "Ессен"]

    return city_list
