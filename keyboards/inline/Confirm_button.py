from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.misc.language_types import F_language

post_callback = CallbackData("questions", "action")


def button(language: str):
    confirm = InlineKeyboardMarkup()
    confirm.row(
        InlineKeyboardButton(
            text=F_language(answer="Подтвердить отправку", language=language),
            callback_data=post_callback.new(action='confirm')),
        InlineKeyboardButton(
            text=F_language(answer="Отмена", language=language),
            callback_data=post_callback.new(action='cancel'))
    )
    return confirm

