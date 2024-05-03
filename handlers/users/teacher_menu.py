from aiogram.dispatcher import FSMContext
import aiogram
from aiogram.utils.exceptions import BotBlocked
from loader import dp, bot, db
from aiogram import types
from keyboards.inline.teacher_confirm_button import teacher_menu
from aiogram.utils.markdown import hcode
from states.teacher_state import Teacher
from aiogram.dispatcher.filters import Command
from utils.misc.language_types import F_language


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('q_'))
async def make_answer(call: types.CallbackQuery, state: FSMContext):
    code = call.data.split("_")[1]
    if db.check_existance(table="answers", criteria="code", id=int(code)) is None:
        await Teacher.GetAnswer.set()
        async with state.proxy() as data:
            data['code'] = int(code)
        question = db.get_from_table(element="question", table="questions", unique="code", argument=code)
        ans = f"Ответьте на этот вопрос с кодом: {hcode(code)}\n Сам вопрос: {question}"
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
            receiver = db.get_from_table(element="id", table="questions", unique="code", argument=code)
            question = db.get_from_table(element="question", table="questions", unique="code", argument=code)
            # get_id = db.get_from_table(element="id", table="questions", unique="code", argument=code)
            answer = (receiver, question, data['answer'], code)
            db.insert_into_table(table="answers", values=answer)
            response = str(F_language(answer="Получен ответ на вопрос: ",
                                      language=db.get_language(id=receiver))) + f"{question}:\n{data['answer']}"
            await bot.send_message(chat_id=receiver, text=response)
        await call.answer(text="Ответ отправлен", show_alert=True)
        await call.message.edit_reply_markup()
        await state.finish()
    except aiogram.utils.exceptions.BotBlocked:
        await call.message.edit_reply_markup()
        await call.answer(text="Студент заблокировал бота. Ответ не был передан.")


@dp.message_handler(Command("delete_answers"))
async def delete_ans(msg: types.Message):
    await msg.answer(text="База вопросов удалена")
