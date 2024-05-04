from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

Posting_bot = "6678980972:AAGLknjNI8nB0yHHLCOG9_hYytyXY7z0LI0"
Questions_bot = "7196106888:AAG1v1ncrexwL2pgWO7PbPDrPqeAj-YmZdE"

BOT_TOKEN = "5424116057:AAFut2pIxoyD0Ty3Lc_rCjffXTzyZh9Erno"
ADMINS = [5928962311]  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = "52.91.95.42"  # Тоже str, но для айпи адреса хоста
WEBAPP_HOST = f"https://{IP}"
WEBAPP_PORT = 8443
WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBAPP_HOST}:{WEBAPP_PORT}{WEBHOOK_PATH}'


banned_users = [5928962311]
