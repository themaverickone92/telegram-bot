from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import IN_DEVELOPMENT_MESSAGE, ACCESS_DENIED_MESSAGE
from database import Database
from services.ozon import OzonService
from services.yandex_market import YandexMarketService
from services.three_pl import ThreePLService

db = Database()
ozon_service = OzonService()
yandex_market_service = YandexMarketService()
three_pl_service = ThreePLService()

async def handle_operations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик операций с маркетплейсами"""
    query = update.callback_query
    await query.answer()
    
    if not query.data:
        return
    
    user_id = query.from_user.id
    operation = query.data
    
    # Получаем текущее состояние пользователя
    user_state = db.get_user_state(user_id)
    marketplace = user_state.get('marketplace') if user_state else None
    
    if not marketplace:
        await query.message.reply_text("Пожалуйста, сначала выберите маркетплейс")
        return
    
    # Проверяем права пользователя
    if not db.check_user_permission(user_id, operation):
        await query.message.reply_text(ACCESS_DENIED_MESSAGE)
        return
    
    # Обработка операций в зависимости от маркетплейса
    if marketplace == 'OZON':
        await handle_ozon_operation(update, operation)
    elif marketplace == 'YANDEX_MARKET':
        await handle_yandex_market_operation(update, operation)
    elif marketplace == 'THREEPL':
        await handle_three_pl_operation(update, operation)
    else:
        await query.message.reply_text(IN_DEVELOPMENT_MESSAGE)

async def handle_ozon_operation(update: Update, operation: str):
    """Обработка операций Ozon"""
    query = update.callback_query
    
    if operation == 'UPDATE_FBS':
        # Логика обновления остатков FBS
        await query.message.reply_text("Функция обновления остатков FBS в разработке")
    elif operation == 'DELETE_FBS':
        # Логика удаления остатков FBS
        await query.message.reply_text("Функция удаления остатков FBS в разработке")
    elif operation == 'SET_CARGO':
        # Логика установки грузомест
        await query.message.reply_text("Функция установки грузомест в разработке")
    else:
        await query.message.reply_text(IN_DEVELOPMENT_MESSAGE)

async def handle_yandex_market_operation(update: Update, operation: str):
    """Обработка операций Яндекс.Маркет"""
    query = update.callback_query
    
    if operation == 'GET_HIDDEN_OFFERS':
        # Получение скрытых товаров с остатками
        await query.message.reply_text("Получение скрытых товаров с остатками...")
        try:
            hidden_offers = await yandex_market_service.get_hidden_offers_with_stocks()
            if hidden_offers:
                message = "Скрытые товары с остатками:\n\n"
                for offer in hidden_offers:
                    message += f"ID: {offer['id']}\nНазвание: {offer['name']}\nОстаток: {offer['stock']}\n\n"
                await query.message.reply_text(message)
            else:
                await query.message.reply_text("Скрытых товаров с остатками не найдено")
        except Exception as e:
            await query.message.reply_text(f"Ошибка при получении скрытых товаров: {str(e)}")
    else:
        await query.message.reply_text(IN_DEVELOPMENT_MESSAGE)

async def handle_three_pl_operation(update: Update, operation: str):
    """Обработка операций 3PL"""
    query = update.callback_query
    
    if operation == '3PL_EXPORT_STOCKS':
        # Экспорт остатков со складов 3PL
        await query.message.reply_text("Начинаю выгрузку остатков со складов 3PL...")
        try:
            stocks = await three_pl_service.export_stocks()
            if stocks:
                # Отправляем файл с остатками
                await query.message.reply_document(
                    document=stocks,
                    filename='3pl_stocks.xlsx',
                    caption="Выгрузка остатков со складов 3PL завершена"
                )
            else:
                await query.message.reply_text("Нет данных для выгрузки")
        except Exception as e:
            await query.message.reply_text(f"Ошибка при выгрузке остатков: {str(e)}")
    else:
        await query.message.reply_text(IN_DEVELOPMENT_MESSAGE) 