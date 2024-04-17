from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

teacher_callback = CallbackData("questions", "action", "code")


def teacher_menu(code: int):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Подтвердить отправку", callback_data=f"t_{code}"),
        InlineKeyboardButton(text="Отменить", callback_data="cancel")
    )
    return markup


mailing_callback = CallbackData("mailing", "action")

confirm_keys = InlineKeyboardMarkup()

confirm_keys.add(
    InlineKeyboardButton(text="Подтвердить отправку", callback_data=mailing_callback.new(action="confirm")),
    InlineKeyboardButton(text="Отменить", callback_data=mailing_callback.new(action="cancel"))
)
