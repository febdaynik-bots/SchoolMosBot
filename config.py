import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())
