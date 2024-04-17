from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.misc.language_types import F_language

buttons = InlineKeyboardMarkup()


def key(language: str):
    buttons.add(InlineKeyboardButton(
        text=F_language(answer="Отмена", language=language), callback_data="cancel"
    ))
    return buttons
