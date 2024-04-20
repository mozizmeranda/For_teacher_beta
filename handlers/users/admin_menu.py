from loader import dp, bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime
from keyboards.inline.answer_key import question_button
from states.mailing_state import Mailing
from keyboards.inline.teacher_confirm_button import mailing_callback, confirm_keys
from aiogram.utils.markdown import hbold
from utils.db_api.students_registration import db_students
import aiogram
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Command
from data.config import ADMINS


def seconds_to_time(seconds):
    time = datetime.fromtimestamp(seconds)
    return time


@dp.message_handler(text="Найти вопрос 🔍")
async def find_question(message: types.Message, state: FSMContext):
    if message.from_user.id == int(ADMINS[0]):
        await message.answer("Пожалуйста отправьте мне код вопроса.")
        # await bot.send_message(i, text="Пожалуйста отправьте мне код вопроса.")
        await state.set_state("find_question")
    else:
        await message.answer("Чего? Я вас не понимаю.")


@dp.message_handler(text="Hello")
async def get_hello(message: types.Message):
    await message.answer("Hello")


@dp.message_handler(state="find_question")
async def show_question(message: types.Message, state: FSMContext):
    if db.check_existance(table="answers", criteria="code", id=int(message.text)):
        student = db.get_from_table(element="student", table="questions", unique="code", argument=int(message.text))
        question = db.get_from_table(element="question", table="questions", unique="code", argument=int(message.text))
        answer = db.get_from_table(element="answer", table="answers", unique="code", argument=int(message.text))
        ans = (f"Вопрос задал: {student}\n"
               f"Вопрос задан: {seconds_to_time(int(message.text))}\n"
               f"Сам вопрос: {question}\n"
               f"Ответ на этот вопрос: {answer}\n"
               f"Статус: Отвечен")
        await message.answer(text=ans)
        await state.finish()
    elif db.check_existance(table="questions", criteria="code", id=int(message.text)):
        student = db.get_from_table(element="student", table="questions", unique="code", argument=int(message.text))
        question = db.get_from_table(element="question", table="questions", unique="code", argument=int(message.text))
        ans = (f"Вопрос задал: {student}\n"
               f"Вопрос задан: {seconds_to_time(int(message.text))}\n"
            f"Сам вопрос: {question}\n"
            f"Статус: Не отвечен.")
        await message.answer(text=ans, reply_markup=question_button(question_code=int(message.text)))
        await state.finish()
    else:
        await message.answer("Вопроса с таким кодом нету")
        await state.finish()


@dp.message_handler(text="Сделать рассылку")
async def make_mailing(message: types.Message, state: FSMContext):
    await message.answer(text="Пришлите текст, который вы хотите разослать всем студентам")
    await Mailing.GetText.set()


@dp.message_handler(state=Mailing.GetText)
async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    question = hbold("Вы точно хотите всем разослать этот текст ?")
    await message.reply(f"{question} \n {message.text}", reply_markup=confirm_keys)
    await Mailing.next()


@dp.callback_query_handler(mailing_callback.filter(action="confirm"), state=Mailing.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        for i in db_students.get_all_students():
            try:
                await bot.send_message(chat_id=i[0], text=data['text'])
                await call.answer(text="Рассыла проведена успешно", show_alert=True)
                try:
                    pass
                except aiogram.utils.exceptions.MessageNotModified:
                    await call.message.edit_reply_markup()
                    await state.finish()
            except aiogram.utils.exceptions.BotBlocked or aiogram.utils.exceptions.MessageNotModified:
                pass


@dp.message_handler(Command("delete_answers"))
async def delete_answers(message: types.Message):
    db.delete_table(table="answers")
    await message.answer("База ответов удалена")

@dp.callback_query_handler(mailing_callback.filter(action="cancel"), state=Mailing.Confirm)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Рассылка отменена", show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()


