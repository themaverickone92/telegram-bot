from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import OPERATION_BUTTONS, THREEPL_BUTTONS, IN_DEVELOPMENT_MESSAGE, ACCESS_DENIED_MESSAGE
from database import Database

db = Database()

async def handle_marketplace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора маркетплейса"""
    query = update.callback_query
    await query.answer()
    
    if not query.data:
        return
    
    user_id = query.from_user.id
    marketplace = query.data
    
    # Проверяем права пользователя
    if not db.check_user_permission(user_id, marketplace):
        await query.message.reply_text(ACCESS_DENIED_MESSAGE)
        return
    
    # Сохраняем выбранный маркетплейс в состоянии пользователя
    db.set_user_state(user_id, {'marketplace': marketplace})
    
    # Формируем клавиатуру в зависимости от выбранного маркетплейса
    if marketplace == 'THREEPL':
        keyboard = [[InlineKeyboardButton(text, callback_data=key)] 
                   for key, text in THREEPL_BUTTONS.items()]
    else:
        keyboard = [[InlineKeyboardButton(text, callback_data=key)] 
                   for key, text in OPERATION_BUTTONS.items()]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с кнопками операций
    await query.message.edit_text(
        f"Выбран маркетплейс: {marketplace}\nВыберите операцию:",
        reply_markup=reply_markup
    ) 