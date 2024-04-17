from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
channels = [-1001944359018]
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

banned_users = [5928962311]
