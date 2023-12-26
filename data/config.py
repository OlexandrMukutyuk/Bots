from environs import Env

env = Env()

env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")

SERVER_BASE_URL: str = env.str("SERVER_BASE_URL")
SERVER_TOKEN: str = env.str("SERVER_TOKEN")

WEBSITE_URL: str = env.str("WEBSITE_URL")
