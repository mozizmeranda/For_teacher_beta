from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get('PORT'))
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'https:/forteacherbot-96867b4c4706.herokuapp.com/webhook/{BOT_TOKEN}'


banned_users = [5928962311]
