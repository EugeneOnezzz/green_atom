from aiogram import types


async def user_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    choose_button = types.KeyboardButton(text="Выбрать направление 🔍")
    train_button = types.KeyboardButton(text="Стажировка 👨‍💻")
    info_button = types.KeyboardButton(text="FAQ 👀")
    profile_button = types.KeyboardButton(text="Профиль 🙋‍♂️")
    # shop_button = types.KeyboardButton(text="Плюшки 🔥") Не успев ((
    quest_button = types.KeyboardButton(text="Задать вопрос 📜")

    markup.add(choose_button, train_button)
    markup.add(info_button, profile_button, quest_button)

    return markup


async def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mail_button = types.KeyboardButton(text="Почта 📪")
    send_button = types.KeyboardButton(text="Рассылка 📨")

    markup.add(mail_button)
    markup.add(send_button)

    return markup
