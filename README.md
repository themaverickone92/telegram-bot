# Yandex Cloud VM Telegram Bot

Простой Telegram бот для приветствия пользователей в Yandex Cloud VM.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd yf_telegram_bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройка Yandex Lockbox:

   a. Создайте секрет в Yandex Lockbox:
   - Откройте консоль Yandex Cloud
   - Перейдите в сервис Lockbox
   - Создайте новый секрет
   - Добавьте ключ `TELEGRAM_TOKEN` со значением вашего токена бота
   - Скопируйте ID секрета

   b. Получение ID секрета:
   - При деплое в Yandex Cloud VM можно получить ID секрета из метаданных инстанса
   - Или передать ID секрета через переменные окружения при деплое
   - В коде замените `your-secret-id` на реальный ID секрета

4. Настройте сервисный аккаунт:
   - Создайте сервисный аккаунт в Yandex Cloud
   - Назначьте ему роль `lockbox.payloadViewer`
   - Создайте авторизованный ключ для сервисного аккаунта
   - Сохраните ключ в файл `key.json`

## Запуск

```bash
python bot.py
```

## Использование

- `/start` - Начать работу с ботом
- `/help` - Показать список доступных команд

## Требования

- Python 3.7+
- python-telegram-bot
- python-dotenv
- yandexcloud