from aiogram.utils import executor
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.students_registration import db_students
from utils.db_api.questions_answers import answers

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    try:
        db.main_db()
        db_students.create_table_users()
        answers.create_table_users()
    except Exception as e:
        print(e)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

