from aiogram.utils import executor
from loader import dp, db, bot
import middlewares, filters, handlers
from aiogram import types
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data import config
from aiohttp import web
import asyncio

async def on_startup(dispatcher):
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    await set_default_commands(dispatcher)
    try:
        db.main_db()
    except Exception as e:
        print(e)
    # Notify about startup
    await on_startup_notify(dispatcher)


async def process_telegram_update(update):
    await dp.process_update(update)


async def handle(request):
    if request.match_info.get('token') == config.BOT_TOKEN:
        data = await request.json()
        update = types.Update(**data)
        await dp.process_update(update)
        return web.Response(text="OK")
    else:
        return web.Response(text="Invalid token")

async def on_shutdown(dp):
    await dp.bot.delete_webhook()


if __name__ == '__main__':
    executor.start_webhook(dispatcher=dp, webhook_path='', skip_updates=True, on_startup=on_startup,
                                 on_shutdown=on_shutdown, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
