# Initialize Bot instance with a default parse mode which will be passed to all API calls
from aiogram import Bot
from aiogram.enums import ParseMode

from data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
