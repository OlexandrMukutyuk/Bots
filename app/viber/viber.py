from data import config
from viberio.api.client import ViberBot
from viberio.types import BotConfiguration

bot_config = BotConfiguration(auth_token=config.BOT_TOKEN, name="Test bot")
viber = ViberBot(bot_config)
