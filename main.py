import asyncio
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from PyToday import database
from PyToday.handlers import start_command, handle_callback, handle_message, broadcast_command
from PyToday import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application):
    await database.init_db()
    logger.info("MongoDB database initialized successfully")

def main():
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not set in environment variables!")
        print("ERROR: Please set BOT_TOKEN environment variable")
        print("Get your bot token from @BotFather on Telegram")
        return
    
    if not config.MONGODB_URI:
        logger.error("MONGODB_URI not set in environment variables!")
        print("ERROR: Please set MONGODB_URI environment variable")
        return
    
    application = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot started successfully!")
    print("Join t.me/PythonTodayz for more bots.")
    
    application.run_polling(allowed_updates=["message", "callback_query"], drop_pending_updates=True)

if __name__ == "__main__":
    main()
