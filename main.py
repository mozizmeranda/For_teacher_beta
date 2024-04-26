import asyncio
from loader import bot, dp
from data import config
from aiogram.utils.executor import start_webhook


async def on_startup(dp):
    await bot.set_webhook(url=config.WEBHOOK_URL)

    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands
    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dispatcher):
    await dispatcher.bot.delete_webhook()

def fu():
    from handlers import dp
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT
    )


if __name__ == "__main__":
    asyncio.run(fu())

