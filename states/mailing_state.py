from aiogram.dispatcher.filters.state import State, StatesGroup



class Mailing(StatesGroup):
    GetText = State()
    Confirm = State()