#!/bin/bash

# Путь к проекту
PROJECT_DIR="$HOME/telegram-bot"

# Переходим в директорию проекта
cd "$PROJECT_DIR"

# Создание виртуального окружения, если его нет
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Установка зависимостей
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

# Создание systemd сервиса
sudo tee /etc/systemd/system/telegram-bot.service > /dev/null << EOL
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$HOME/telegram-bot
Environment="PATH=$HOME/telegram-bot/venv/bin"
ExecStart=$HOME/telegram-bot/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Перезагрузка systemd и запуск сервиса
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl restart telegram-bot

echo "Deployment completed successfully" 