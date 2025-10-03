import os
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверяем, что токен загружен
if not BOT_TOKEN:
    print("❌ ОШИБКА: TELEGRAM_BOT_TOKEN не найден в .env файле!")
    print("📝 Убедитесь, что файл .env существует и содержит:")
    print("   TELEGRAM_BOT_TOKEN=ваш_токен")
    exit(1)

user_cooldowns = {}
card_phrases = [
    "хуйня карта 0/10",
    "норм карта 5/10", 
    "имба карта 10/0 айгиз оценит"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 Бот запущен! Используй /getcard")

async def getcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()

    if user_id in user_cooldowns:
        time_passed = current_time - user_cooldowns[user_id]
        if time_passed < 60:
            remaining = int(60 - time_passed)
            await update.message.reply_text(f"⏳ Кулдаун! Жди {remaining} сек.")
            return

    user_cooldowns[user_id] = current_time
    random_phrase = random.choice(card_phrases)
    await update.message.reply_text(f"🎴 {random_phrase}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getcard", getcard))
    
    print("✅ Токен загружен успешно!")
    print("🤖 Бот запущен на Replit!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

