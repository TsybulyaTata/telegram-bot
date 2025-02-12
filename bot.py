import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Отримуємо API-токен з оточення
TOKEN = os.getenv("TOKEN")

# Перевіряємо, чи є токен
if not TOKEN:
    raise ValueError("TOKEN не знайдено! Перевір API-токен.")

# Створюємо бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привіт! Я твій Telegram-бот. Напиши мені щось!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Ти написав: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
