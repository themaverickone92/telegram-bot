import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from yandexcloud import SDK
from yandexcloud.operation import OperationError

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_config_from_lockbox():
    """Get all configuration from Yandex Lockbox."""
    try:
        # Initialize SDK
        sdk = SDK()
        
        # Get Lockbox service
        lockbox_service = sdk.client(LockboxServiceClient)
        
        # Get secret payload
        # В реальном приложении ID секрета можно получить из метаданных инстанса
        # или передавать через переменные окружения при деплое
        secret_id = "your-secret-id"  # Замените на реальный ID секрета
        response = lockbox_service.get_payload(secret_id=secret_id)
        
        # Создаем словарь с конфигурацией
        config = {}
        for entry in response.entries:
            config[entry.key] = entry.text_value
                
        if "TELEGRAM_TOKEN" not in config:
            raise ValueError("TELEGRAM_TOKEN not found in Lockbox secret")
            
        return config
        
    except Exception as e:
        logger.error(f"Error getting configuration from Lockbox: {e}")
        raise

# Get configuration from Lockbox
config = get_config_from_lockbox()
TOKEN = config["TELEGRAM_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! 👋\n\n'
        'Добро пожаловать в Yandex Cloud VM! 🚀\n'
        'Я ваш помощник для работы с виртуальной машиной.\n\n'
        'Используйте /help для получения списка доступных команд.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать это сообщение'
    )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 