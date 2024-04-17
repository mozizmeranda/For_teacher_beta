from aiogram.dispatcher.filters.state import StatesGroup, State


class Questionioning(StatesGroup):
    Theme = State()
    Question = State()
    Confirm = State()
