from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def question_button(question_code: int):
    answer = InlineKeyboardMarkup()
    answer.add(
        InlineKeyboardButton(text="Ответить", callback_data=f"q_{question_code}")
    )
    return answer

