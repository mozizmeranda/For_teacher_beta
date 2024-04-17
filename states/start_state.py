from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    Language = State()
    Group = State()
    Name = State()
