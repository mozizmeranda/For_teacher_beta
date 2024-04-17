from aiogram.dispatcher.filters.state import StatesGroup, State


class Teacher(StatesGroup):
    GetAnswer = State()
    Confirm = State()
