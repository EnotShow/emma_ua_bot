def user_questionnaire_template(age, name, city, about):
    """Шаблон акеты пользователя"""
    return f'{name}, {age}, {city}\n.\n{about}'


def user_international_questionnaire_template(age, name, country, city, about):
    """Шаблон интернациональной анкеты пользователя """
    return f'{name}, {age}, {city}, {country}\n.\n{about}'
