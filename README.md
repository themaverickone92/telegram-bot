# Telegram Bot for Marketplace Operations

Телеграм-бот для управления операциями с маркетплейсами (Ozon, Яндекс.Маркет, Wildberries) и 3PL складами.

## Функциональность

- Управление остатками FBS
- Установка грузомест
- Экспорт остатков со складов 3PL
- Получение информации о скрытых товарах
- Система ролей и прав доступа

## Требования

- Python 3.8+
- Yandex Cloud VM
- Yandex Database
- Telegram Bot Token

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/telegram-bot.git
cd telegram-bot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Настройте Yandex Cloud Secrets Manager:

   a. Создайте сервисный аккаунт в Yandex Cloud:
   ```bash
   yc iam service-account create --name telegram-bot-sa
   ```

   b. Назначьте роли сервисному аккаунту:
   ```bash
   yc resource-manager folders add-access-binding default \
     --role secretmanager.secrets.versionAdder \
     --subject serviceAccount:<service-account-id>
   ```

   c. Создайте секреты в Lockbox:
   ```bash
   # Секрет с токеном бота
   yc secrets create --name yf-oper-bot --data TELEGRAM_TOKEN=your_bot_token

   # Секрет с конфигурацией Yandex Cloud
   yc secrets create --name yf-cloud-config --data '{
     "YC_SERVICE_ACCOUNT_ID": "your-service-account-id",
     "YC_KEY_ID": "your-key-id",
     "YC_PRIVATE_KEY": "your-private-key",
     "YD_ENDPOINT": "your-ydb-endpoint",
     "YD_PATH": "your-ydb-path"
   }'
   ```

## Деплой на Yandex Cloud VM

1. Создайте виртуальную машину в Yandex Cloud

2. Скопируйте скрипт деплоя на VM:
```bash
scp deploy.sh user@your-vm-ip:/tmp/
```

3. Подключитесь к VM и выполните скрипт:
```bash
ssh user@your-vm-ip
cd /tmp
chmod +x deploy.sh
./deploy.sh
```

## Структура проекта

```
telegram-bot/
├── src/
│   ├── bot.py              # Основной класс бота
│   ├── config.py           # Конфигурация
│   ├── database.py         # Работа с базой данных
│   ├── handlers/           # Обработчики команд
│   │   ├── marketplace.py
│   │   ├── operations.py
│   │   ├── documents.py
│   │   └── roles.py
│   └── services/          # Сервисы для работы с API
│       ├── ozon.py
│       ├── yandex_market.py
│       └── three_pl.py
├── requirements.txt       # Зависимости
├── deploy.sh             # Скрипт деплоя
└── README.md            # Документация
```

## Использование

1. Запустите бота:
```bash
python src/main.py
```

2. В Telegram отправьте команду `/start` для начала работы

3. Используйте меню для выбора маркетплейса и операции

## Управление ролями

Для управления ролями пользователей используйте команду:
```
/setrole <user_id> <role>
```

Доступные роли:
- ADMIN
- REPLENISHMENT
- LOGISTICS
- VIEWER

## Логирование

Логи сохраняются в файл `bot.log` и выводятся в stdout.

## Безопасность

- Все конфиденциальные данные хранятся в Yandex Cloud Secrets Manager (Lockbox):
  - Токен Telegram бота
  - Данные для доступа к Yandex Cloud
  - Конфигурация Yandex Database
- Доступ к операциям контролируется системой ролей
- Бот использует сервисный аккаунт с минимально необходимыми правами

## Поддержка

При возникновении проблем создайте issue в репозитории проекта. 