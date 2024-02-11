from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import os

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())
