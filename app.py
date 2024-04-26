from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from data import config


async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    db.main_db()
    # Notify about startup
    await on_startup_notify(dispatcher)


async def on_startup_handler():
    await on_startup(dp)


async def on_shutdown(dispatcher):
    await dp.bot.delete_webhook()


async def process_telegram_update(update):
    await dp.process_update(update)


if __name__ == '__main__':
    executor.start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
