# from aiogram import Bot, Dispatcher, types
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.callback_data import CallbackData
#
# callback = CallbackData("fruits", "fruit_type")
# buttons = InlineKeyboardMarkup()
# buttons.add(
#     InlineKeyboardButton(text="Фрукты", callback_data=callback.new())
# )


def func_decor(func):
    def wrapper():
        print("Что-то делает")
        func()
        print("что делает после вызова функции")
    return wrapper


def some_func():
    print("some_func")


f = func_decor(some_func)
f()