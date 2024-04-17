import asyncio

from aiogram import types, Dispatcher
from typing import Union

from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware) :
    def __init__(self, limit = DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return
        dp = Dispatcher.get_current()
        limit = getattr(handler, "throttling_rate_limit", self.limit)
        key = getattr(handler, "throttlingkey", f"{self.prefix}_{handler.__name__}")

        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(self, target: Union[types.Message, types.CallbackQuery], throttled: Throttled, dispatcher: Dispatcher, key: str):
        if isinstance(target, types.CallbackQuery):
            msg = target.message
            delta = throttled.rate - throttled.delta
        else:
            target

        if throttled.exceeded_count == 2:
            await msg.reply('too many clicks')
            return
        elif throttled == 3:
            await msg.reply(f"I won't answer you, I'll reply after {delta}")
            return
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply('now will start answering')

        async def on_process_message(self, message, data):
            await self.throttle(message)

        async def on_process_callbackquery(self, call, data):
            await self.throttle(call)


