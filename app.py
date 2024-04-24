from aiogram.utils import executor
from loader import dp, db
import middlewares, filters, handlers
from aiogram import types
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config

async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    await set_default_commands(dispatcher)
    try:
        db.main_db()
    except Exception as e:
        print(e)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def process_telegram_update(update):
    await dp.process_update(update)


async def handle(request):
    if request.match_info.get('token') == config.BOT_TOKEN:
        data = await request.json()
        update = types.Update(**data)
        await dp.process_update(update)
    else:
        print("Doesn't work")

async def on_startup_handler():
    await on_startup(dp)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


# async def on_startup(dispatcher):
#     # Устанавливаем дефолтные команды
#     await set_default_commands(dispatcher)
#     try:
#         db.main_db()
#     except Exception as e:
#         print(e)
#
#     # Уведомляет про запуск
#     await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown,
                            host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
    # executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

