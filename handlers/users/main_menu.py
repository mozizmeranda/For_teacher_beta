from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from utils.db_api.Questions import questions
from aiogram.dispatcher.filters import Command
from utils.misc.language_types import F_language
from utils.db_api.students_registration import db_students
from states.question_state import Questionioning
from keyboards.inline.Confirm_button import button, post_callback
from keyboards.inline.answer_key import question_button
from datetime import datetime
from aiogram.utils.markdown import hcode


@dp.message_handler(Command("delete_questions"))
async def get_command(message: types.Message):
    questions.delete_all()
    await message.answer("Успешно удалено")


@dp.message_handler(Command("question"))
async def begin(message: types.Message):
    if db_students.check(message.from_user.id) is not None:
        await message.answer(text=F_language(answer="Напишите несколько слов про тему вашего вопроса.\n"
                                                    "Максимум 10 символов.",
                                             language=db_students.get_language(id=message.from_user.id)))
        await Questionioning.Theme.set()
    else:
        await message.answer(text="Пройдите регистрацию")


@dp.message_handler(state=Questionioning.Theme)
async def theme(message: types.Message, state: FSMContext):
    if len(message.text) <= 10:
        async with state.proxy() as data:
            data['theme'] = message.text
        await message.answer(F_language(answer="Теперь пришлите сам вопрос.",
                                        language=db_students.get_language(id=message.from_user.id)))
        await Questionioning.next()
    else:
        await message.answer(F_language(answer="Написано же, что максимум 10 символов!",
                                        language=db_students.get_language(id=message.from_user.id)))


@dp.message_handler(state=Questionioning.Question)
async def get_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
        await message.answer(text=f"{data['theme']}\n \n "
                                  f"{data['question']}")
        await message.answer(text=F_language(answer="Вы точно хотите задать этот вопрос?",
                                             language=db_students.get_language(id=message.from_user.id)),
                             reply_markup=button(language=db_students.get_language(id=message.from_user.id)))
    await Questionioning.next()


@dp.callback_query_handler(post_callback.filter(action="confirm"), state=Questionioning.Confirm)
async def click_confirm(call: types.CallbackQuery, state: FSMContext):
    code = int(datetime.now().timestamp())#%10000000
    async with state.proxy() as data:
        await bot.send_message(chat_id=5928962311, text=f"{data['theme']}\n {data['question']}\n"
                                                        f"Студент: {db_students.get_info(id=call.from_user.id)}\n"
                                                        "code: " + hcode(f"{code}"),
                               reply_markup=question_button(question_code=code))
    async with state.proxy() as data:
        questions.add_question(id=call.message.chat.id, theme=data['theme'], question=data['question'],
                               code=code, student=db_students.get_info(id=call.from_user.id))
        await call.message.answer(text=f"Code: {code}")
        await call.answer(text=F_language(answer="Вопрос успешно отправлен.",
                                          language=db_students.get_language(call.message.from_user.id)))
    await call.message.edit_reply_markup()
    await state.finish()


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=Questionioning.Confirm)
async def make_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(F_language(answer="Вы отменили отправку вопроса. Чтобы отправить вопрос, "
                                                "вам надо заново задать его, нажав другую кнопку.",
                                         language=db_students.get_language(call.from_user.id)))
    await state.finish()
    