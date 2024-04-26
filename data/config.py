from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "7196106888:AAG1v1ncrexwL2pgWO7PbPDrPqeAj-YmZdE"  # Забираем значение типа str
ADMINS = [5928962311]  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = "localhost"  # Тоже str, но для айпи адреса хоста
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get('PORT'))
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBAPP_HOST}{WEBHOOK_PATH}'


banned_users = [5928962311]
