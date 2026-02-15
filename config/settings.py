# -*- coding: utf-8 -*-
"""
Конфігураційні налаштування для Agro Marketplace Bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Завантаження .env файлу з кореня проекту
PROJECT_ROOT = Path(__file__).resolve().parents[1]
env_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=env_path)

# Telegram Bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено в .env файлі!")

# Адміністратори
ADMIN_IDS_STR = os.getenv('ADMIN_IDS', '')
ADMIN_IDS = [int(id.strip()) for id in ADMIN_IDS_STR.split(',') if id.strip().isdigit()]

# База даних - єдина для бота і веб-панелі
DB_FILE = os.getenv('DB_FILE', 'data/agro_bot.db')
# Перетворюємо на абсолютний шлях
DB_PATH = PROJECT_ROOT / DB_FILE if not os.path.isabs(DB_FILE) else Path(DB_FILE)

# Flask Web Panel
FLASK_SECRET = os.getenv('FLASK_SECRET', 'super-secret-key-change-me')
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'admin123')

# Логування
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
