#!/bin/bash

# Проверка наличия необходимых переменных окружения
if [ -z "$YC_SERVICE_ACCOUNT_ID" ] || [ -z "$YC_KEY_ID" ] || [ -z "$YC_PRIVATE_KEY" ]; then
    echo "Error: Required environment variables are not set"
    exit 1
fi

# Создание директории для проекта
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Клонирование репозитория
git clone https://github.com/your-username/telegram-bot.git .

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Создание файла с переменными окружения
cat > .env << EOL
YC_SERVICE_ACCOUNT_ID=$YC_SERVICE_ACCOUNT_ID
YC_KEY_ID=$YC_KEY_ID
YC_PRIVATE_KEY=$YC_PRIVATE_KEY
YD_ENDPOINT=$YD_ENDPOINT
YD_PATH=$YD_PATH
EOL

# Создание systemd сервиса
cat > /etc/systemd/system/telegram-bot.service << EOL
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Перезагрузка systemd и запуск сервиса
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot

echo "Deployment completed successfully" 