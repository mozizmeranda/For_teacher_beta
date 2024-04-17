from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

question = KeyboardButton(text="Найти вопрос 🔍")
statistics = KeyboardButton(text="Сделать рассылку")
teachers_buttons = ReplyKeyboardMarkup(keyboard=[[question, statistics]], resize_keyboard=True, one_time_keyboard=True)
