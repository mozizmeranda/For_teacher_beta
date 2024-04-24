from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.misc.language_types import F_language
from states.question_state import Questionioning
from keyboards.inline.Confirm_button import button, post_callback
from keyboards.inline.answer_key import question_button
from datetime import datetime
from aiogram.utils.markdown import hcode, hbold
from data.config import ADMINS


@dp.message_handler(Command("delete_questions"))
async def get_command(message: types.Message):
    db.delete_table(table="questions")
    await message.answer("Успешно удалено")


@dp.message_handler(text="Задать вопрос")
@dp.message_handler(text="Savol berish")
async def begin(message: types.Message):
    if db.check_existance(table="Users", criteria="id", id=message.from_user.id) is not None:
        await message.answer(text=F_language(answer="Напишите несколько слов про тему вашего вопроса.\n"
                                                    "Максимум 15 символов.",
                                                language=db.get_language(id=message.from_user.id)))
        await Questionioning.Theme.set()
    else:
        await message.answer(text="Пройдите регистрацию")


@dp.message_handler(state=Questionioning.Theme)
async def theme(message: types.Message, state: FSMContext):
    if len(message.text) <= 15:
        async with state.proxy() as data:
            data['theme'] = message.text
        await message.answer(F_language(answer="Теперь пришлите сам вопрос.",
                                        language=db.get_language(id=message.from_user.id)))
        await Questionioning.next()
    else:
        await message.answer(F_language(answer="Написано же, что максимум 15 символов!",
                                        language=db.get_language(id=message.from_user.id)))


@dp.message_handler(state=Questionioning.Question)
async def get_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
        await message.answer(text=f"{hbold(data['theme'])}\n \n "
                                  f"{data['question']}")
        await message.answer(text=F_language(answer="Вы точно хотите задать этот вопрос?",
                                             language=db.get_language(id=message.from_user.id)),
                             reply_markup=button(language=db.get_language(id=message.from_user.id)))
    await Questionioning.next()


@dp.callback_query_handler(post_callback.filter(action="confirm"), state=Questionioning.Confirm)
async def click_confirm(call: types.CallbackQuery, state: FSMContext):
    code = int(datetime.now().timestamp())#%10000000
    async with state.proxy() as data:
        for i in ADMINS:
            question = f"{data['theme']}\n {data['question']}\nСтудент: {db.get_from_table(element='full_name', table='Users', unique='id', argument=call.from_user.id)}"
            await bot.send_message(chat_id=i, text=question, reply_markup=question_button(question_code=code))
    async with state.proxy() as data:
        student_name = db.get_from_table(element="full_name", table="Users", unique="id", argument=call.from_user.id)
        student_group = db.get_from_table(element="group_name", table="Users", unique="id", argument=call.from_user.id)
        student = f"Имя: {student_name}, Группа: {student_group}"
        question = (call.message.chat.id, data['theme'], data['question'], student, code)
        db.insert_into_table(table="questions", values=question)
        text = F_language(answer="Код вашего вопроса: ", language=db.get_language(id=call.from_user.id))
        sending_code = text + str(code)
        await call.message.answer(text=sending_code)
        await call.answer(text=F_language(answer="Вопрос успешно отправлен.",
                                          language=db.get_language(id=call.from_user.id)))
    await call.message.edit_reply_markup()
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=Questionioning.Confirm)
async def make_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(F_language(answer="Вы отменили отправку вопроса. Чтобы отправить вопрос, вам надо заново задать его, нажав другую кнопку.",
                                         language=db.get_language(id=call.from_user.id)))
    await call.message.edit_reply_markup()
    await state.finish()
    