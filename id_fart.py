import os
import random
import time
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Безопасное получение токена
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Настройки (замените эти значения)
YOUR_USER_ID = 5195824376  # ЗАМЕНИТЕ на ваш Telegram ID
TARGET_CHAT_ID = None  # Будет определено автоматически или установлено вручную
BOT_USERNAME = "Gimart_bot"  # Юзернейм вашего бота

user_cooldowns = {}
card_phrases = [
    "хуйня карта 0/10",
    "норм карта 5/10",
    "имба карта 10/0 айгиз оценит"
]

# Переменная для хранения задачи авто-отправки
auto_send_task = None
# Словарь для хранения ID чатов
chat_ids = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/getcard пропиши епта"
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения ID чата"""
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title or "Личный чат"
    

    
    # Сохраняем ID чата для авто-отправки
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = chat_id
    print(f"💾 ID чата сохранен: {chat_id}")

async def set_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установить текущий чат для авто-отправки"""
    global TARGET_CHAT_ID
    
    # Проверяем права
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("❌ Эта команда только для владельца бота")
        return
    
    TARGET_CHAT_ID = update.effective_chat.id
    chat_title = update.effective_chat.title or "этот чат"
    

async def getcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()

    # Проверка кулдауна
    if user_id in user_cooldowns:
        time_passed = current_time - user_cooldowns[user_id]
        if time_passed < 60:
            remaining = int(60 - time_passed)
            await update.message.reply_text(f"⏳ Кулдаун! Жди {remaining} сек.")
            return

    # Обновляем время и отправляем карту
    user_cooldowns[user_id] = current_time
    random_phrase = random.choice(card_phrases)
    await update.message.reply_text(f"🎴 {random_phrase}")

async def autosend_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск автоматической отправки каждые 3 часа"""
    global auto_send_task, TARGET_CHAT_ID
    
    # Проверяем права
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("❌ Эта команда только для владельца бота")
        return
    
    # Проверяем, установлен ли ID чата
    if not TARGET_CHAT_ID:
        await update.message.reply_text(
            "❌ ID чата не установлен!\n"
            "Добавьте бота в группу и используйте:\n"
            "/set_chat - установить этот чат\n"
            "/getid - узнать ID чата"
        )
        return
    
    if auto_send_task and not auto_send_task.done():
        await update.message.reply_text("✅ Авто-отправка уже запущена")
        return
    
    # Запускаем задачу
    auto_send_task = asyncio.create_task(auto_send_loop(context))

async def autosend_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Остановка автоматической отправки"""
    global auto_send_task
    
    # Проверяем права
    if update.effective_user.id != YOUR_USER_ID:
        await update.message.reply_text("❌ Эта команда только для владельца бота")
        return
    
    if auto_send_task and not auto_send_task.done():
        auto_send_task.cancel()
        await update.message.reply_text("🛑 Авто-отправка остановлена")
    else:
        await update.message.reply_text("ℹ️ Авто-отправка не была запущена")

async def auto_send_loop(context: ContextTypes.DEFAULT_TYPE):
    """Цикл автоматической отправки сообщений каждые 3 часа"""
    global TARGET_CHAT_ID
    
    try:
        while True:
            # Отправляем команду от вашего имени
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=f"/getcard@{BOT_USERNAME}"
            )
            
            next_time = datetime.now() + timedelta(hours=3)
            
            # Ждем 3 часа (10800 секунд)
            await asyncio.sleep(10800)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getcard", getcard))
    application.add_handler(CommandHandler("getid", get_id))
    application.add_handler(CommandHandler("set_chat", set_chat))
    application.add_handler(CommandHandler("autosend_start", autosend_start))
    application.add_handler(CommandHandler("autosend_stop", autosend_stop))
    
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
