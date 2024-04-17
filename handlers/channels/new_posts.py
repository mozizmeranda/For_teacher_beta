from aiogram import types
from loader import dp
import logging

@dp.channel_post_handler(content_types=types.ContentType.ANY)
async def new_post(message: types.Message):
    logging.info(f"It was published a new post in a channel {message.chat.title}: \n"
                 f"{message.text}")