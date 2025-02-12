import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Логування для відстеження помилок
logging.basicConfig(level=logging.INFO)

# Отримуємо API-токен з середовищних змінних
TOKEN = os.getenv("TOKEN")

# Перевіряємо, чи є токен
if not TOKEN:
    raise ValueError("TOKEN не знайдено! Перевір API-токен.")

# Створюємо бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привіт! Я твій Telegram-бот. Напиши мені щось!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Ти написав: {message.text}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
