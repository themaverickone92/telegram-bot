import os
import sys
import logging
from bot import TelegramBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска бота"""
    try:
        # Проверяем наличие необходимых переменных окружения
        required_env_vars = [
            'YC_SERVICE_ACCOUNT_ID',
            'YC_KEY_ID',
            'YC_PRIVATE_KEY',
            'YD_ENDPOINT',
            'YD_PATH'
        ]
        
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Создаем и запускаем бота
        bot = TelegramBot()
        logger.info("Starting bot...")
        bot.run()
        
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 