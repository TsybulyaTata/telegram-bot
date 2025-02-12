import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Отримуємо API-токен з оточення
TOKEN = os.getenv("TOKEN")

# Перевіряємо, чи є токен
if not TOKEN:
    raise ValueError("TOKEN не знайдено! Перевір API-токен.")

# Створюємо бота та диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Використовуємо Router для обробки команд
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привіт! Я твій Telegram-бот. Напиши мені щось!")

@router.message()
async def echo(message: Message):
    await message.answer(f"Ти написав: {message.text}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
