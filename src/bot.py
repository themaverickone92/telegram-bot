import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import (
    BOT_TOKEN, MARKETPLACE_BUTTONS, OPERATION_BUTTONS, THREEPL_BUTTONS,
    WELCOME_MESSAGE, IN_DEVELOPMENT_MESSAGE, UPLOAD_FILE_MESSAGE, SUCCESS_MESSAGE,
    ACCESS_DENIED_MESSAGE, USER_ROLES, ROLE_PERMISSIONS, ADMIN_IDS
)
from handlers.marketplace import handle_marketplace
from handlers.operations import handle_operations
from handlers.documents import handle_document
from handlers.roles import set_role
from database import Database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        """Инициализация бота"""
        if not BOT_TOKEN:
            raise ValueError("Не удалось получить токен бота из Yandex Cloud Secrets")
        
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.db = Database()
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд"""
        # Основные команды
        self.application.add_handler(CommandHandler(['start', 'menu'], self.start))
        self.application.add_handler(CommandHandler('setrole', set_role))
        
        # Обработчики callback-запросов
        self.application.add_handler(CallbackQueryHandler(handle_marketplace, pattern='^(YANDEX_MARKET|OZON|WB|THREEPL)$'))
        self.application.add_handler(CallbackQueryHandler(handle_operations, pattern='^(UPDATE_FBS|DELETE_FBS|PLAN_FBO|SET_CARGO|GET_HIDDEN_OFFERS|3PL_EXPORT_STOCKS)$'))
        
        # Обработчик документов
        self.application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        
        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        keyboard = [[InlineKeyboardButton(text, callback_data=key)] 
                   for key, text in MARKETPLACE_BUTTONS.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Очищаем предыдущее состояние пользователя
        self.db.clear_user_state(update.effective_user.id)
        
        await update.message.reply_photo(
            photo='https://storage.yandexcloud.net/yf-storage/welcome.png',
            caption=WELCOME_MESSAGE.format(username=update.effective_user.first_name),
            reply_markup=reply_markup
        )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
            )

    def run(self):
        """Запуск бота"""
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run() 