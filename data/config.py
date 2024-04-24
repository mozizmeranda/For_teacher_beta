from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = "7196106888:AAGgLiOaJPZigL2AZfoPx1Mf-Wi1qU6CxmU"  # Забираем значение типа str
ADMINS = [5928962311]  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = "localhost"  # Тоже str, но для айпи адреса хоста
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get('PORT'))
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'https:/forteacherbot-96867b4c4706.herokuapp.com/webhook/{BOT_TOKEN}'


banned_users = [5928962311]
