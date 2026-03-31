Проект: tele_bot
Регистрационный бот для сбора заявок на сайте flask.cubinez.ru. Проводит пользователя по пошаговому сценарию: приветствие → кнопка → ссылка на сайт → подтверждение регистрации.
🎯 Основные функции
✅ Пошаговый сценарий регистрации:
   1. Приветствие + стикер/изображение
   2. Кнопка "🔗 Кнопка" → отправка ссылки
   3. Кнопка "✅ Кнопка 2" → подтверждение регистрации

✅ Мультиплатформенность:
   • Telegram-бот (pyTelegramBotAPI / telebot)
   • VK-бот (vkbottle) с кнопками-ссылками

✅ Интеграция с внешним сайтом:
   • Отправка ссылки на flask.cubinez.ru
   • Кнопка OpenLink в VK для прямого перехода в браузер

✅ Гибкая конфигурация:
   • Токены в .env
   • URL сайта настраивается через переменную окружения
🚀 Запуск через systemd
Telegram-бот
# /etc/systemd/system/tele_bot.service
[Unit]
Description=Telegram Registration Bot
After=network.target

[Service]
User=cubinez85
Group=cubinez85
WorkingDirectory=/home/cubinez85/tele_bot
Environment="PATH=/home/cubinez85/tele_bot/venv/bin"
ExecStart=/home/cubinez85/tele_bot/venv/bin/python /home/cubinez85/tele_bot/bot_service.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target

VK-бот
# /etc/systemd/system/tele_bot-vk.service
[Unit]
Description=VK Registration Bot
After=network.target

[Service]
User=cubinez85
Group=cubinez85
WorkingDirectory=/home/cubinez85/tele_bot
Environment="PATH=/home/cubinez85/tele_bot/venv/bin"
ExecStart=/home/cubinez85/tele_bot/venv/bin/python /home/cubinez85/tele_bot/bot_vk.py
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target

🛠️ Техническое обслуживание
# Проверка статуса
sudo systemctl status tele_bot tele_bot-vk

# Логи
journalctl -u tele_bot -f
journalctl -u tele_bot-vk -f

# Перезапуск
sudo systemctl restart tele_bot
sudo systemctl restart tele_bot-vk

# Если Telegram заблокирован — включить прокси:
# 1. Установить: pip install pysocks
# 2. В .env: USE_PROXY=1
# 3. В bot.py добавить настройку apihelper.proxy

# 4. Перезапустить: sudo systemctl restart tele_bot
