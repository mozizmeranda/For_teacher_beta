from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from aiogram import types
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config
import asyncio

async def on_startup(dispatcher):
    await bot.set_webhook(config.WEBHOOK_URL)
    await set_default_commands(dispatcher)
    try:
        db.main_db()
    except Exception as e:
        print(e)
    # Notify about startup
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()

async def run_bot():
    await executor.start_webhook(dispatcher=dp, webhook_path='', skip_updates=True, on_startup=on_startup,
                                  on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
