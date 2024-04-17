from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = InlineKeyboardMarkup()

buttons.add(
InlineKeyboardButton(text=f"O'zbek tili 🇺🇿", callback_data=f"l_uz"),
    InlineKeyboardButton(text=f"Русский язык 🇷🇺", callback_data=f"l_ru")
)