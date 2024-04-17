from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.db_api.Questions import questions
from utils.db_api.questions_answers import answers
from datetime import datetime
from keyboards.inline.answer_key import question_button
from states.mailing_state import Mailing
from keyboards.inline.teacher_confirm_button import mailing_callback, confirm_keys
from aiogram.utils.markdown import hbold
from utils.db_api.students_registration import db_students
import aiogram
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Command


def seconds_to_time(seconds):
    time = datetime.fromtimestamp(seconds)
    time_gmt5 = time
    return time_gmt5.strftime('%H:%M:%S %A %B %Y')


@dp.message_handler(Command("Get_all"))
async def test(message: types.Message):
    for i in db_students.get_all_students():
        await message.answer(text=f"{i[0]}")


@dp.message_handler(text="Найти вопрос 🔍")
async def find_question(message: types.Message, state: FSMContext):
    if message.from_user.id == 5928962311:
        await message.answer("Пожалуйста отправьте мне код вопроса.")
        await state.set_state("find_question")
    else:
        await message.answer("Чего? Я вас не понимаю.")


@dp.message_handler(state="find_question")
async def show_question(message: types.Message, state: FSMContext):
    if questions.check_existence(code=int(message.text)) is not None:
        ans = (f"Вопрос задал: {questions.get_student(code=int(message.text))[0]}\n"
               f"Вопрос задан: {seconds_to_time(int(message.text))}\n"
            f"Сам вопрос: {questions.get_question(code=int(message.text))[0]}"
            f"Статус: Не отвечан.")
        await message.answer(text=ans, reply_markup=question_button(question_code=int(message.text)))
        await state.finish()
    elif answers.check(code=int(message.text)) is not None: #add questions
        ans = (f"Вопрос задал: {answers.get_student(code=int(message.text))}\n"
               f"Вопрос задан: {seconds_to_time(int(message.text))}\n"
               f"Сам вопрос: {answers.get_question(code=int(message.text))}\n"
               f"Ответ на этот вопрос: {answers.get_answer(code=int(message.text))}\n"
               f"Статус: Отвечан")
        await message.answer(text=ans)
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


@dp.callback_query_handler(mailing_callback.filter(action="cancel"), state=Mailing.Confirm)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Рассылка отменена", show_alert=True)
    await state.finish()


