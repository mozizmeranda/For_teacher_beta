from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.misc.language_types import F_language


def kbs(language: str):
    button1 = KeyboardButton(text=F_language(answer="Отправить файл на проверку", language=language))
    button2 = KeyboardButton(text=F_language(answer="Задать вопрос", language=language))
    mark = ReplyKeyboardMarkup(keyboard=[
        [
            button1,
            button2
        ]
    ], resize_keyboard=True, one_time_keyboard=True)

    return mark
