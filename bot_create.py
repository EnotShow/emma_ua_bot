from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

db = MemoryStorage()

bot = Bot(token='5218712793:AAGyqbqXRicF-zyMilG-Z6No3C32B5JWfBA')
dp = Dispatcher(bot, storage=db)
