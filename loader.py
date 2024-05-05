from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.Questions import DataBase
import ssl
from data import config

db = DataBase()
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_certificate = open(config.WEBHOOK_SSL_CERT, "rb").read()
ssl_context.load_cert_chain(config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_KEY)
