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

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Получите токен для вашего бота у [@BotFather](https://t.me/BotFather) в Telegram и добавьте его в файл `.env`:
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

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