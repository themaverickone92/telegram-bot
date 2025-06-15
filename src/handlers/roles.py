from telegram import Update
from telegram.ext import ContextTypes
from config import ROLE_PERMISSIONS, ADMIN_IDS, ACCESS_DENIED_MESSAGE
from database import Database

db = Database()

async def set_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды установки роли пользователя"""
    # Проверяем, является ли пользователь администратором
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(ACCESS_DENIED_MESSAGE)
        return
    
    # Проверяем наличие аргументов
    if not context.args or len(context.args) != 2:
        await update.message.reply_text(
            "Использование: /setrole <user_id> <role>\n"
            "Доступные роли: ADMIN, REPLENISHMENT, LOGISTICS, VIEWER"
        )
        return
    
    try:
        user_id = int(context.args[0])
        role = context.args[1].upper()
        
        # Проверяем существование роли
        if role not in ROLE_PERMISSIONS:
            await update.message.reply_text(
                f"Неизвестная роль: {role}\n"
                "Доступные роли: ADMIN, REPLENISHMENT, LOGISTICS, VIEWER"
            )
            return
        
        # Устанавливаем роль пользователя
        success = db.set_user_role(user_id, role)
        if success:
            await update.message.reply_text(f"Роль {role} успешно установлена для пользователя {user_id}")
        else:
            await update.message.reply_text(f"Ошибка при установке роли для пользователя {user_id}")
            
    except ValueError:
        await update.message.reply_text("ID пользователя должен быть числом")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при установке роли: {str(e)}") 