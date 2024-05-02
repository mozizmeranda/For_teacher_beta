from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config

# async def on_startup(dispatcher):
#     await set_default_commands(dispatcher)
#     try:
#         await db.main_db()
#     except Exception as e:
#         print(e)
#
#     # db.delete_users()
#     await on_startup_notify(dispatcher)


async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    await set_default_commands(dispatcher)
    try:
        await db.main_db()
    except Exception as e:
        print(e)

    await on_startup_notify(dispatcher)


async def on_startup_handler():
    await on_startup(dp)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


if __name__ == "__main__":
    executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH, on_startup=on_startup,
                           on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

