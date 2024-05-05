import asyncio
from aiogram import executor
from loader import dp, db, bot, ssl_certificate
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config
#
#
async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL, certificate=ssl_certificate)
    try:
        await db.main_db()
    except Exception as e:
        print("Error initializing database:", e)
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(on_startup(dp))
        executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH,
                               on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT,
                               ssl_certificate=ssl_certificate)
    except Exception as e:
        print("Error:", e)
        loop.run_until_complete(on_shutdown(dp))
