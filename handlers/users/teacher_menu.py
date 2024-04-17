from aiogram.dispatcher import FSMContext
import aiogram
from aiogram.utils.exceptions import BotBlocked
from loader import dp, bot
from aiogram import types
from utils.db_api.Questions import questions
from keyboards.inline.teacher_confirm_button import teacher_menu
from aiogram.utils.markdown import hcode
from states.teacher_state import Teacher
from utils.db_api.questions_answers import answers
from aiogram.dispatcher.filters import Command
from utils.misc.language_types import F_language
from utils.db_api.students_registration import db_students


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('q_'))
async def make_answer(call: types.CallbackQuery, state: FSMContext):
    code = call.data.split("_")[1]
    if answers.check(code=code) is None:
        await Teacher.GetAnswer.set()
        async with state.proxy() as data:
            data['code'] = int(code)
        ans = f"Ответьте на этот вопрос с кодом: {hcode(code)}\n Сам вопрос: {questions.get_question(code=code)[0]}"
        await call.message.answer(text=ans)
        await call.message.edit_reply_markup()
    else:
        await call.message.edit_reply_markup()
        await call.answer(text="Вы уже ответили на этот вопрос")


@dp.message_handler(state=Teacher.GetAnswer)
async def ans_from_teacher(message: types.Message, state: FSMContext):
    try:
        await message.answer(text=message.text)
        async with state.proxy() as data:
            data['answer'] = message.text
            c = data['code']
            await message.answer(text="Вы точно хотите отправить этот ответ ?", reply_markup=teacher_menu(code=c))
        await Teacher.next()
    except aiogram.utils.exceptions.BotBlocked:
        pass


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('t_'), state=Teacher.Confirm)
async def confirm_from_teacher(call: types.CallbackQuery, state: FSMContext):
    try:
        code = call.data.split("_")[1]
        async with state.proxy() as data:
            answers.add_answer(question=questions.get_question(code=data['code'])[0], code=data['code'],
                               student=questions.get_student(code=data['code'])[0], answer=data['answer'])
            receiver = questions.get_receiver(code=code)
            response = str(F_language(answer="Получен ответ на вопрос: ",
                                  language=db_students.get_language(id=questions.get_id(code=data['code'])))) + (f"{questions.get_question(code=data['code'])[0]}: \n"
                                                                                                                 f"{data['answer']}")
            await bot.send_message(chat_id=receiver[0], text=response)
            questions.delete_question(code=data['code'])
        await call.answer(text="Ответ отправлен", show_alert=True)
        await call.message.edit_reply_markup()
        await state.finish()
    except aiogram.utils.exceptions.BotBlocked:
        await call.message.edit_reply_markup()
        await call.answer(text="Студент заблокировал бота. Ответ не был передан.")


@dp.message_handler(Command("delete_answers"))
async def delete_ans(msg: types.Message):
    answers.delete_all()
    await msg.answer(text="База вопросов удалена")
