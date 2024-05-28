from aiogram.dispatcher.filters.state import StatesGroup, State


class Questionioning(StatesGroup):
    Theme = State()
    Text = State()
    Photo = State()
    Video = State()
    File = State()
    Question = State()
    Confirm = State()


class Questioning_photo(StatesGroup):
    photo = State()
    Question = State()
    Confirm = State()