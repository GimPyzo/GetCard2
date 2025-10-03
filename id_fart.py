import os
import random
import time
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Веб-сервер для поддержания активности
app = Flask('')

@app.route('/')
def home():
    return "и восстали машины из пепла ядерного огня"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# Безопасное получение токена
BOT_TOKEN = os.environ['BOT_TOKEN']

user_cooldowns = {}
card_phrases = [
    "хуйня карта 0/10",
    "норм карта 5/10",
    "имба карта 10/0 айгиз оценит"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/getcard пропишите дауны")

async def getcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()

    if user_id in user_cooldowns:
        time_passed = current_time - user_cooldowns[user_id]
        if time_passed < 60:
            remaining = int(60 - time_passed)
            await update.message.reply_text(f"КУЛДААУННН {remaining} сек.")
            return

    user_cooldowns[user_id] = current_time
    random_phrase = random.choice(card_phrases)
    await update.message.reply_text(f"🎴 {random_phrase}")

def main():
    # Запускаем веб-сервер для поддержания активности
    keep_alive()
    
    # Создаем приложение бота
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getcard", getcard))
    
    print("🤖 Бот запущен на Replit!")
    print("🌐 Keep-alive сервер активен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()


