import os
from dotenv import load_dotenv
from yandexcloud import SDK
import json

# Загрузка переменных окружения (если нужно)
load_dotenv()

# ID секретов
YC_SECRET_ID = 'yc_key'           # Секрет с YC_SERVICE_ACCOUNT_ID, YC_KEY_ID, YC_PRIVATE_KEY
YDB_SECRET_ID = 'yf-ydb-sec'      # Секрет с YD_ENDPOINT, YD_PATH
BOT_SECRET_ID = 'yf-oper-bot'     # Секрет с TELEGRAM_TOKEN

# Инициализация SDK Yandex Cloud
sdk = SDK()

def get_secret(secret_id: str) -> dict:
    """Получение секрета из Yandex Cloud Secrets Manager"""
    try:
        secret = sdk.secrets().get_secret(secret_id)
        return secret.payload
    except Exception as e:
        print(f"Error getting secret {secret_id}: {e}")
        return {}

# Получаем значения из секретов
yc_secret = get_secret(YC_SECRET_ID)
ydb_secret = get_secret(YDB_SECRET_ID)
bot_secret = get_secret(BOT_SECRET_ID)

# Токен бота
BOT_TOKEN = bot_secret.get('TELEGRAM_TOKEN')

# Конфигурация Yandex Cloud
YC_SERVICE_ACCOUNT_ID = yc_secret.get('YC_SERVICE_ACCOUNT_ID')
YC_KEY_ID = yc_secret.get('YC_KEY_ID')
YC_PRIVATE_KEY = yc_secret.get('YC_PRIVATE_KEY')

# Конфигурация YDB
YD_ENDPOINT = ydb_secret.get('YD_ENDPOINT')
YD_PATH = ydb_secret.get('YD_PATH')

# API конфигурация
OZON_API_KEY = os.getenv('OZON_API_KEY')
OZON_CLIENT_ID = os.getenv('OZON_CLIENT_ID')
OZON_API_URL = 'https://api-seller.ozon.ru/v1/cargoes/create'
OZON_INFO_URL = 'https://api-seller.ozon.ru/v1/cargoes/create/info'

# Яндекс Маркет API конфигурация
YANDEX_MARKET_TOKEN = os.getenv('YANDEX_MARKET_TOKEN')
YANDEX_MARKET_CAMPAIGN_ID = os.getenv('YANDEX_MARKET_CAMPAIGN_ID')
YANDEX_MARKET_API_URL = 'https://api.partner.market.yandex.ru'

# Константы для меню
MARKETPLACE_BUTTONS = {
    'YANDEX_MARKET': '🚚 Яндекс Маркет',
    'OZON': '📘 Ozon',
    'WB': '🛍️ Wildberries',
    'THREEPL': '📦 3PL'
}

OPERATION_BUTTONS = {
    'UPDATE_FBS': '🔄 Обновить остатки FBS',
    'DELETE_FBS': '🗑️ Удалить остатки FBS',
    'PLAN_FBO': '📅 Запланировать поставку FBO',
    'SET_CARGO': '🖨️ Установка грузомест',
    'GET_HIDDEN_OFFERS': '📦 Скрытые товары с остатками'
}

THREEPL_BUTTONS = {
    '3PL_EXPORT_STOCKS': '📤 Скачать остатки'
}

# Сообщения
WELCOME_MESSAGE = "Привет, {username}! Выбери маркетплейс"
IN_DEVELOPMENT_MESSAGE = "Функция в разработке"
UPLOAD_FILE_MESSAGE = "Пожалуйста, загрузите файл с упаковочными листами в формате xlsx"
SUCCESS_MESSAGE = "Грузоместа для поставки {supply_id} успешно установлены!"
ACCESS_DENIED_MESSAGE = "У вас нет прав для выполнения этой операции"

# Роли пользователей
USER_ROLES = {
    'OZON': {
        'permissions': ['UPDATE_FBS', 'DELETE_FBS', 'SET_CARGO', 'PRINT_LABEL', 'SKIP_LABEL']
    },
    'WB': {
        'permissions': ['UPDATE_FBS', 'DELETE_FBS']
    },
    'THREEPL': {
        'permissions': ['3PL_EXPORT_STOCKS']
    },
    'YANDEX_MARKET': {
        'permissions': ['GET_HIDDEN_OFFERS']
    }
}

# Права доступа для ролей
ROLE_PERMISSIONS = {
    'ADMIN': ['*'],  # Полный доступ
    'REPLENISHMENT': ['UPDATE_FBS', 'PLAN_FBO', '3PL_EXPORT_STOCKS', 'OZON', 'WB'],
    'LOGISTICS': ['SET_CARGO', '3PL_EXPORT_STOCKS', 'OZON', 'WB', 'THREEPL'],
    'VIEWER': ['3PL_EXPORT_STOCKS', 'THREEPL']
}

# Администраторы системы
ADMIN_IDS = [819594325]  # Список ID администраторов 