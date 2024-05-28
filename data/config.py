from environs import Env
import os

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

Posting_bot = "6678980972:AAGLknjNI8nB0yHHLCOG9_hYytyXY7z0LI0"
Questions_bot = "7196106888:AAG1v1ncrexwL2pgWO7PbPDrPqeAj-YmZdE"
testing_bot = "5424116057:AAFut2pIxoyD0Ty3Lc_rCjffXTzyZh9Erno"

BOT_TOKEN = testing_bot
ADMINS = [5928962311]  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = "52.91.95.42"  # Тоже str, но для айпи адреса хоста
WEBAPP_HOST = f"https://{IP}"
WEBAPP_PORT = 8443
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBAPP_HOST}:{WEBAPP_PORT}{WEBHOOK_PATH}'


# WEBHOOK_SSL_CERT = "webhook_cert.pem"
# WEBHOOK_SSL_KEY = "webhook_key.pem"

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DATABASE = env.str("DATABASE")
banned_users = [5928962311]

postgres_url = f"postgres://{DB_USER}:{DB_PASS}@{IP}:5432/{DATABASE}"

banned_users = [5928962311]
