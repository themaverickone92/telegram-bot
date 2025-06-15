from telegram import Update
from telegram.ext import ContextTypes
from config import UPLOAD_FILE_MESSAGE
from database import Database
from services.ozon import OzonService
import pandas as pd
from io import BytesIO

db = Database()
ozon_service = OzonService()

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик загрузки документов"""
    user_id = update.effective_user.id
    user_state = db.get_user_state(user_id)
    
    if not user_state:
        await update.message.reply_text("Пожалуйста, сначала выберите операцию")
        return
    
    # Получаем информацию о документе
    document = update.message.document
    if not document:
        await update.message.reply_text("Пожалуйста, отправьте файл")
        return
    
    # Проверяем расширение файла
    if not document.file_name.endswith('.xlsx'):
        await update.message.reply_text("Пожалуйста, отправьте файл в формате .xlsx")
        return
    
    # Скачиваем файл
    file = await context.bot.get_file(document.file_id)
    file_bytes = await file.download_as_bytearray()
    
    try:
        # Читаем Excel файл
        df = pd.read_excel(BytesIO(file_bytes))
        
        # Обрабатываем файл в зависимости от операции
        if user_state.get('operation') == 'SET_CARGO':
            await handle_cargo_file(update, df)
        elif user_state.get('operation') == 'UPDATE_FBS':
            await handle_fbs_file(update, df)
        else:
            await update.message.reply_text("Неизвестная операция")
            
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке файла: {str(e)}")

async def handle_cargo_file(update: Update, df: pd.DataFrame):
    """Обработка файла с грузоместами"""
    try:
        # Проверяем наличие необходимых колонок
        required_columns = ['supply_id', 'cargo_id']
        if not all(col in df.columns for col in required_columns):
            await update.message.reply_text("Файл должен содержать колонки: supply_id, cargo_id")
            return
        
        # Обрабатываем каждую строку
        for _, row in df.iterrows():
            supply_id = row['supply_id']
            cargo_id = row['cargo_id']
            
            # Устанавливаем грузоместо
            success = await ozon_service.set_cargo(supply_id, cargo_id)
            if not success:
                await update.message.reply_text(f"Ошибка при установке грузоместа для поставки {supply_id}")
                continue
        
        await update.message.reply_text("Грузоместа успешно установлены")
        
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке файла с грузоместами: {str(e)}")

async def handle_fbs_file(update: Update, df: pd.DataFrame):
    """Обработка файла с остатками FBS"""
    try:
        # Проверяем наличие необходимых колонок
        required_columns = ['product_id', 'stock']
        if not all(col in df.columns for col in required_columns):
            await update.message.reply_text("Файл должен содержать колонки: product_id, stock")
            return
        
        # Обновляем остатки
        success = await ozon_service.update_fbs_stocks(df)
        if success:
            await update.message.reply_text("Остатки FBS успешно обновлены")
        else:
            await update.message.reply_text("Ошибка при обновлении остатков FBS")
            
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке файла с остатками: {str(e)}") 