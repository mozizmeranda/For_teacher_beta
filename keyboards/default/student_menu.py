from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.misc.language_types import F_language


def menu(language: str):
    question = KeyboardButton(text=F_language("Задать вопрос", language=language))
    buttons = ReplyKeyboardMarkup(keyboard=[[question]], resize_keyboard=True, one_time_keyboard=True)
    return buttons
