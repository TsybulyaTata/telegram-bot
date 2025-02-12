import os
import logging
import asyncio
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher
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

# Підключення до Google Sheets через змінну середовища
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.getenv("GOOGLE_CREDENTIALS"))  # Беремо креденшіали з оточення
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Відкриваємо таблицю за її ID
SPREADSHEET_ID = "15JoTTwrYoIztMFrdPfZ5FJwE3ZuNYs4w09-tD5hD12Q"  # ВСТАВ СВІЙ ID ТАБЛИЦІ
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Створюємо бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Використовуємо Router для обробки команд
router = Router()
dp.include_router(router)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привіт! Введи назву міста, і я скажу приблизну вартість поїздки.")

@router.message()
async def get_city_price(message: Message):
    city = message.text.strip()
    data = sheet.get_all_records()

    for row in data:
        if row["Місто"] == city:
            response = (
                f"📍 {city}\n"
                f"🏨 Готель: {row['Готель']} грн\n"
                f"🚕 Проїзд: {row['Проїзд']} грн\n"
                f"💰 Добові: {row['Добові']} грн\n"
            )
            await message.answer(response)
            return
    
    await message.answer("❌ Вибач, але я не знайшов інформації про це місто.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

