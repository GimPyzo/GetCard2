import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Словарь для хранения времени последнего использования команды
user_cooldowns = {}

# Список фраз для выдачи
card_phrases = [
    "хуйня карта 0/10",
    "норм карта 5/10", 
    "имба карта 10/0 айгиз оценит"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/getcard пропиште дауны")

async def getcard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_time = time.time()
    
    # Проверяем кулдаун
    if user_id in user_cooldowns:
        time_passed = current_time - user_cooldowns[user_id]
        if time_passed < 60:  # 60 секунд = 1 минута
            await update.message.reply_text("ЭЭЭУУ КУЛДАУН ЩА")
            return
    
    # Обновляем время последнего использования
    user_cooldowns[user_id] = current_time
    
    # Выбираем случайную фразу
    random_phrase = random.choice(card_phrases)
    await update.message.reply_text(random_phrase)

def main():
    # Замени 'TOKEN' на токен твоего бота от @BotFather
    application = Application.builder().token("6600731008:AAG9FuI5wKKwtFuYnKXkPAGBKB5o4VjfSSg").build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getcard", getcard))
    
    # Запускаем бота
    print("Я ЖИВОЙ")
    application.run_polling()

if __name__ == "__main__":
    main()
