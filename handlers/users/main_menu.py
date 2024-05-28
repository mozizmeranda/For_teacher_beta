from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from aiogram import types
from states.question_state import Questionioning
from aiogram.dispatcher.filters import Command
from utils.misc.language_types import F_language
from states.question_state import Questionioning
from keyboards.inline.Confirm_button import button, post_callback
from keyboards.inline.answer_key import question_button
from datetime import datetime
from aiogram.utils.markdown import hcode
from data.config import ADMINS
from datetime import datetime


@dp.message_handler(Command("delete_questions"))
async def get_command(message: types.Message):
    db.delete_table(table="questions")
    await message.answer("Успешно удалено")


@dp.message_handler(text="Задать вопрос")
@dp.message_handler(text="Savol berish")
async def begin(message: types.Message):
    if db.check_existance(table="Users", criteria="id", id=message.from_user.id) is not None:
        await message.answer(text=F_language(answer="Напишите несколько слов про тему вашего вопроса.\n"
                                                    "Максимум 15 символов. "
                                                    "Или можете прислать фотографию без текста как тему.",
                                             language=db.get_language(id=message.from_user.id)))
        await Questionioning.Theme.set()
    else:
        await message.answer(text="Пройдите регистрацию")


@dp.message_handler(content_types=types.ContentTypes.ANY, state=Questionioning.Theme)
async def question_start(message: types.Message, state: FSMContext):
    if message.photo:
        await Questionioning.Photo.set()
        async with state.proxy() as data:
            data['Photo'] = message.photo[0].file_id
        await Questionioning.Photo.set()
        await message.answer(text=F_language(answer="Теперь пришлите сам вопрос.",
                                             language=db.get_language(message.from_user.id)))
    if message.text:
        await Questionioning.Text.set()
        async with state.proxy() as data:
            data['document_id'] = message.text
        await Questionioning.Text.set()
        await message.answer(text=F_language(answer="Теперь пришлите сам вопрос.",
                                             language=db.get_language(message.from_user.id)))

    if message.document:
        await Questionioning.File.set()
        async with state.proxy() as data:
            data['document_id'] = message.document.file_id
        await Questionioning.File.set()
        await message.answer(text=F_language(answer="Теперь пришлите сам вопрос.",
                                             language=db.get_language(message.from_user.id)))


@dp.message_handler(content_types=types.ContentTypes.TEXT, state="*")
async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if await state.get_state() == "Questionioning:Photo":
            await message.answer(text=f"{await state.get_state()}")
            key = await state.get_state()
            data['question'] = message.text
            await message.answer(F_language(answer="Вы точно хотите задать этот вопрос?",
                                            language=db.get_language(message.from_user.id)))
            await bot.send_photo(chat_id=message.from_user.id, photo=data[key.split(":")[1]], caption=data['question'],
                                 reply_markup=button(language=db.get_language(id=message.from_user.id)))
        if await state.get_state() == "Questionioning:Text":
            await message.answer(text=f"{await state.get_state()}")
            key = await state.get_state()
            data['question'] = message.text
            await message.answer(F_language(answer="Вы точно хотите задать этот вопрос?",
                                            language=db.get_language(message.from_user.id)))
            await message.answer(text=f"{data['theme']} \n{data['question']}")
        if message.document == "Questionioning:File":
            await message.answer(f"{await state.get_state()}")
            await message.answer(F_language(answer="Вы точно хотите задать этот вопрос?",
                                            language=db.get_language(message.from_user.id)))
            await bot.send_document(chat_id=message.from_user.id, document=data['document_id'], caption=data['question'],
                                    reply_markup=button(language=db.get_language(id=message.from_user.id)))

# @dp.message_handler(state=Questionioning.Theme, content_types=types.ContentTypes.ANY)
# async def theme(message: types.Message, state: FSMContext):
#     if message.text:
#         if len(message.text) <= 15:
#             async with state.proxy() as data:
#                 data['theme'] = message.text
#             await message.answer(F_language(answer="Теперь пришлите сам вопрос.",
#                                             language=db.get_language(id=message.from_user.id)))
#             await Questionioning.next()
#         else:
#             await message.answer(F_language(answer="Написано же, что максимум 15 символов!",
#                                             language=db.get_language(id=message.from_user.id)))
#     if message.photo:
#         async with state.proxy() as data:
#             data['Photo'] = message.photo[0].file_id
#         await message.answer(F_language(answer="Теперь пришлите сам вопрос.",
#                                         language=db.get_language(id=message.from_user.id)))
#         await Questionioning.next()
#
#
# @dp.message_handler(state=Questionioning.Question)
# async def get_question(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if len(data['theme']) < 15:
#             data['question'] = message.text
#             await message.answer(text=f"{hbold(data['theme'])}\n \n"
#                                       f"{data['question']}")
#             await message.answer(text=F_language(answer="Вы точно хотите задать этот вопрос?",
#                                                  language=db.get_language(id=message.from_user.id)),
#                                  reply_markup=button(language=db.get_language(id=message.from_user.id)))
#         else:
#             data['question'] = message.text
#             await bot.send_photo(chat_id=message.from_user.id, photo=data['theme'], caption=data['question'],
#                                  reply_markup=button(language=db.get_language(id=message.from_user.id)))
#         await Questionioning.next()


@dp.callback_query_handler(post_callback.filter(action="confirm"), state="*")
async def click_confirm(call: types.CallbackQuery, state: FSMContext):
    start = datetime.now().timestamp()
    code = int(datetime.now().timestamp())  # %10000000
    student_name = db.get_from_table(element="full_name", table="Users", unique="id", argument=call.from_user.id)
    student_group = db.get_from_table(element="group_name", table="Users", unique="id", argument=call.from_user.id)
    student = f"Имя: {student_name}, Группа: {student_group}"
    async with state.proxy() as data:
        text = F_language(answer="Код вашего вопроса: ", language=db.get_language(id=call.from_user.id))
        key = await state.get_state()
        question = (call.message.chat.id, data[str(key.split(":")[1])], data['question'], student, code)
        db.insert_into_table(table="questions", values=question)
        sending_code = text + str(hcode(code))
        if await state.get_state() == "Questionioning:Photo":
            for i in ADMINS:
                question = (f"{data['question']}\nСтудент: "
                            f"{db.get_from_table(element='full_name', table='Users', 
                                                 unique='id', argument=call.from_user.id)}")
                await bot.send_photo(chat_id=i, photo=data['Photo'], caption=question,
                                     reply_markup=question_button(question_code=code))
        if await state.get_state() == "Questionioning:Text":
            for i in ADMINS:
                question = (f"{data['question']}\nСтудент: "
                            f"{db.get_from_table(element='full_name', table='Users', 
                                                 unique='id', argument=call.from_user.id)}")
                await bot.send_message(chat_id=i, text=question, disable_web_page_preview=True,
                                       reply_markup=question_button(question_code=code))
        if await state.get_state() == "Questionioning:File":
            for i in ADMINS:
                question = (f"{data['question']}\nСтудент: "
                            f"{db.get_from_table(element='full_name', table='Users', 
                                                 unique='id', argument=call.from_user.id)}")
                await bot.send_document(chat_id=i, document=data['document_id'], caption=question,
                                        reply_markup=question_button(question_code=code))
        await call.message.answer(text=sending_code)
        await call.message.edit_reply_markup()
    await state.finish()
    print(f"Execution Time: {datetime.now().timestamp() - start}")
# @dp.callback_query_handler(post_callback.filter(action="confirm"), state=Questionioning.Confirm)
# async def click_confirm(call: types.CallbackQuery, state: FSMContext):
#     code = int(datetime.now().timestamp())  # %10000000
#     student_name = db.get_from_table(element="full_name", table="Users", unique="id", argument=call.from_user.id)
#     student_group = db.get_from_table(element="group_name", table="Users", unique="id", argument=call.from_user.id)
#     student = f"Имя: {student_name}, Группа: {student_group}"
#     async with state.proxy() as data:
#         if len(data['theme']) < 15:
#             text = F_language(answer="Код вашего вопроса: ", language=db.get_language(id=call.from_user.id))
#             question = (call.message.chat.id, data['theme'], data['question'], student, code)
#             db.insert_into_table(table="questions", values=question)
#             sending_code = text + str(hcode(code))
#             await call.message.answer(text=sending_code)
#             await call.message.edit_reply_markup()
#             for i in ADMINS:
#                 question = (f"{data['theme']}\n {data['question']}\nСтудент: "
#                             f"{db.get_from_table(element='full_name',
#                                                  table='Users', unique='id', argument=call.from_user.id)}")
#                 await bot.send_message(chat_id=i, text=question, reply_markup=question_button(question_code=code))
#         else:
#             text = F_language(answer="Код вашего вопроса: ", language=db.get_language(id=call.from_user.id))
#             question = (call.message.chat.id, data['theme'], data['question'], student, code)
#             db.insert_into_table(table="questions", values=question)
#             sending_code = text + str(hcode(code))
#             await call.message.answer(text=sending_code)
#             await call.message.edit_reply_markup()
#             for i in ADMINS:
#                 question = f"{data['question']}\nСтудент: {db.get_from_table(element='full_name',
#                                                                 table='Users', unique='id', argument=call.from_user.id)}"
#                 await bot.send_photo(chat_id=i, photo=data['theme'], caption=question,
#                                      reply_markup=question_button(question_code=code))
#     await call.answer(text=F_language(answer="Вопрос успешно отправлен.",
#                                       language=db.get_language(id=call.from_user.id)))
#     await state.finish()


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=Questionioning.Confirm)
async def make_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(F_language(answer="Вы отменили отправку вопроса. Чтобы отправить вопрос, "  # edited
                                                "вам надо заново задать его, нажав другую кнопку.",
                                         language=db.get_language(id=call.from_user.id)))
    await call.message.edit_reply_markup()
    await state.finish()
    