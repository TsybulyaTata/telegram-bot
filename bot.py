import os
import logging
import asyncio
import json
import gspread
from flask import Flask
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

# Запускаємо фіктивний веб-сервер, щоб Render не вимикав бота
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот працює!"

def run_web_server():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Отримуємо API-токен з оточення
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TOKEN не знайдено! Перевір API-токен в Render.")

# Отримуємо креденшіали Google з оточення
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

if not GOOGLE_CREDENTIALS:
    raise ValueError("❌ GOOGLE_CREDENTIALS не знайдено! Перевір змінні середовища в Render.")

# Підключення до Google Sheets через змінну середовища
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(GOOGLE_CREDENTIALS)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# Відкриваємо Google Таблицю за її ID
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
        if row["Місто"].lower() == city.lower():
            response = (
                f"📍 {city}\n"
                f"🏨 Готель: {row['Готель']} грн\n"
                f"🚕 Проїзд: {row['Проїзд']} грн\n"
                f"💰 Добові: {row['Добові']} грн\n"
            )
            await message.answer(response)
            return
    
    await message.answer("❌ Вибач, але я не знайшов інформації про це місто.")

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаємо Telegram-бот у окремому потоці
    bot_thread = Thread(target=lambda: asyncio.run(start_bot()))
    bot_thread.start()

    # Запускаємо веб-сервер Flask
    run_web_server()
