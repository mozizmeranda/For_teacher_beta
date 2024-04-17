from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
import logging
from data.config import banned_users
from aiogram.dispatcher.handler import CancelHandler

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        #1
        logging.info('first update')
        logging.info('1. pre process update')
        logging.info('2. next is process update')
        data['middleware_data'] = 'this will reach on_post_process'
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            return

        if user in banned_users:
            raise CancelHandler()
    #2
    async def on_process_update(self, update: types.Update, data: dict):
        logging.info(f"2. Process update: {data=}")
        logging.info('След точка : Pre-process message')

    #3
    async def on_pre_process_message(self, message: types.Message, data: dict):
        logging.info(f"3. Pre process message: {data=}")
        logging.info("the next are: Filters, Process message")
        data['middleware_data'] = "this will reach on_process_message"

    #4


    #5
    async def on_process_message(self, message: types.Message, data: dict):
        logging.info(f"4. Process Message")
        logging.info(" the next is Handler")
        data['middleware_data'] = "this will reach Handler"

    #6

    #7
    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        logging.info(f"7. Post process message, {data=}, {data_from_handler}")
        logging.info("the next is Post process update")

    #8
    async def on_post_process_update(self, update: types.Update, data_from_handler: list, data: dict):
        logging.info(f"8. post process Update, {data=}, {data_from_handler=}")