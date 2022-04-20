from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")

USER = env.str("USER_DB")
PASSWORD = env.str("PASSWORD_DB")
HOST = env.str("HOST_DB")
PORT = env.int("PORT_DB")
DATABASE = env.str("NAME_DB")

