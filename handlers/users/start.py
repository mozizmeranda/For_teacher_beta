from loader import dp, db
from states.start_state import Registration
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from keyboards.inline.language_buttons import buttons
from utils.misc.language_types import F_language
from keyboards.default.teacher_keys import teachers_buttons
from keyboards.default.student_menu import menu
from utils.misc.throttling import rate_limit
from keyboards.default.choices import kbs


@dp.message_handler(Command("edit"))
async def edit_data(message: types.Message):
    await message.answer(F_language(answer="Вы вызвали команду для замены ваших данных. "
                                           "Вам придется заново зарегистрироваться.",
                                    language=db.get_language(id=message.from_user.id)))
    db.delete_user(id=message.from_user.id)
    await message.answer(text="Здравствуйте, пожалуйста укажите какой язык вы предпочитаете использовать. \n"
                              "Assalomu alaykum, qaysi tildan foydalanishni afzal ko'rasiz.",
                         reply_markup=buttons)
    await Registration.Language.set()


@dp.message_handler(CommandStart())
@rate_limit(2, 'start')
async def bot_start(message: types.Message):
    if message.from_user.id == 5928962311:
        await message.answer(text="Вы учитель и админ одновременно", reply_markup=teachers_buttons)
    elif db.check_existance(table="Users", criteria="id", id=message.from_user.id) is not None:
        await message.answer(text=F_language(answer="Вы уже зарегестрированы в системе. Для "
                                                    "смены данных вызовите команду /edit.",
                                             language=db.get_language(id=message.from_user.id)),

                             reply_markup=kbs(language=db.get_language(message.from_user.id)))
    else:
        await message.answer(text="Здравствуйте, пожалуйста укажите какой язык вы предпочитаете использовать. \n"
                                  "Assalomu alaykum, qaysi tildan foydalanishni afzal ko'rasiz.",
                             reply_markup=buttons)
        await Registration.Language.set()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('l_'), state=Registration.Language)
async def choose_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data.split("_")[1]  # 'ru' or 'uz'
    await call.message.edit_reply_markup()
    async with state.proxy() as data:
        data['language'] = language
        await call.message.answer(text=F_language(answer="В какой группе вы учитесь? Пример: SI-23-19",
                                                  language=data['language']))
    await Registration.next()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Registration.Group)
async def get_group(message: types.Message, state: FSMContext):
    group = message.text
    async with state.proxy() as data:
        data['group'] = group
        await message.answer(text=F_language(answer="Пожалуйста напишите своё имя с фамилией",
                                             language=data['language']))
    await Registration.next()


@dp.message_handler(state=Registration.Name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name'] = name
        await message.answer(text=F_language(answer="Спасибо, вы успешно прошли регистрацию.",
                                             language=data['language']))
        await message.answer(text=F_language(answer="Вы можете задать вопрос с помощью кнопки ниже.",
                                             language=data['language']),
                             reply_markup=kbs(language=data['language']))
        user = (message.from_user.id, data['group'], data['name'], data['language'])
        db.insert_into_table(table="Users", values=user)
    await state.finish()
