import asyncio
from aiogram import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config


async def on_startup(dispatcher):
    # await dp.bot.set_webhook(config.WEBHOOK_URL, certificate=ssl_certificate)
    try:
        db.main_db()
    except Exception as e:
        print("Error initializing database:", e)
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

#
# async def on_shutdown(dispatcher):
#     await dp.bot.delete_webhook()


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
