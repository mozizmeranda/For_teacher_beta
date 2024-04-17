from loader import dp
from states.start_state import Registration
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from keyboards.inline.language_buttons import buttons
from utils.misc.language_types import F_language
from utils.db_api.students_registration import db_students
from keyboards.default.teacher_keys import teachers_buttons
from keyboards.default.student_menu import menu
from aiogram.utils.markdown import hbold


@dp.message_handler(Command("delete_users"))
async def delete_all_ones(message: types.Message):
    db_students.delete()
    await message.answer(text="Все успешно удалено")


@dp.message_handler(Command("edit"))
async def edit_data(message: types.Message):
    await message.answer(F_language(answer="Вы вызвали команду для замены ваших данных. Вам придется заново зарегистрироваться.",
                                    language=db_students.get_language(id=message.from_user.id)))
    db_students.delete_for_edit(id=message.from_user.id)
    await message.answer(text="Здравствуйте, пожалуйста укажите какой язык вы предпочитаете использовать. \n"
                              "Assalomu alaykum, qaysi tildan foydalanishni afzal ko'rasiz.",
                         reply_markup=buttons)
    await Registration.Language.set()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.id == 5928962311:
        await message.answer(text="Вы учитель и админ одновременно", reply_markup=teachers_buttons)
    else:
        if db_students.check(message.from_user.id) is None:
            await message.answer(text="Здравствуйте, пожалуйста укажите какой язык вы предпочитаете использовать. \n"
                                      "Assalomu alaykum, qaysi tildan foydalanishni afzal ko'rasiz.",
                                 reply_markup=buttons)
            await Registration.Language.set()
        else:
            await message.answer(text="Вы уже зарегестрированы в системе. Чтобы изменить данные вызовите команду /edit\n"
                             "Siz allaqachon tizimda ro'yxatdan o'tgansiz. Ma'lumotlarni o'zgartirish uchun /edit buyrug'ini chaqiring",
                                 reply_markup=menu(language=db_students.get_language(id=message.from_user.id)))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('l_'), state=Registration.Language)
async def choose_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data.split("_")[1] #'ru' or 'uz'
    async with state.proxy() as data:
        data['language'] = language
        await call.message.answer(text=F_language(answer="В какой группе вы учитесь? Пример: SI-23-19", language=data['language']))
    await Registration.next()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Registration.Group)
async def get_group(message: types.Message, state: FSMContext):
    group = message.text
    async with state.proxy() as data:
        data['group'] = group
        await message.answer(text=F_language(answer="Пожалуйста напишите своё имя с фамилией", language=data['language']))
    await Registration.next()


@dp.message_handler(state=Registration.Name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name'] = name
        await message.answer(text=F_language(answer="Спасибо, вы успешно прошли регистрацию.", language=data['language']))
        await message.answer(text=F_language(answer="Вы можете задать вопрос с помощью кнопки ниже.", language=data['language']),
                             reply_markup=menu(language=data['language']))
        db_students.add_student(id=message.from_user.id, group=data['group'], full_name=data['name'], language=data['language'])
    await state.finish()

