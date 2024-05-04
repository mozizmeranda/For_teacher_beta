import asyncio
from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config


async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    await set_default_commands(dispatcher)
    try:
        await db.main_db()
    except Exception as e:
        print("Error initializing database:", e)

    await on_startup_notify(dispatcher)


async def on_startup_handler():
    await on_startup(dp)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


if __name__ == "__main__":
    try:
        executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH, on_startup=on_startup,
                               skip_updates=True, on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
    except Exception as e:
        print("Error starting webhook executor:", e)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(on_shutdown(dp))
