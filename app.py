from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from data import config
from aiogram import Dispatcher
import asyncio


async def on_startup(dispatcher: Dispatcher):
    db.main_db()

    async def startup():
        await dispatcher.bot.set_webhook(config.WEBHOOK_URL)
    await on_startup_notify(dispatcher)
    asyncio.run(startup())
    bot.close()


async def on_startup_handler():
    await on_startup(dp)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


async def process_telegram_update(update):
    await dp.process_update(update)

def main():
    executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)

