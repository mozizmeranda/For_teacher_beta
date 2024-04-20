from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api import students_registration
from utils.db_api.Questions import DataBase

from data import config

db = DataBase()

PROXY_URL = "http://proxy.server:3128"

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
