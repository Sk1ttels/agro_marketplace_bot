"""
Middleware для перевірки статусу бану користувачів
"""

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
import aiosqlite
import logging
import os

logger = logging.getLogger(__name__)

# Отримуємо шлях до БД з конфігурації
try:
    from config.settings import DB_PATH
    DB_FILE = str(DB_PATH)
except:
    DB_FILE = os.getenv("DB_FILE", "data/agro_bot.db")


class BanCheckMiddleware(BaseMiddleware):
    """Middleware для перевірки чи користувач заблокований"""
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Отримати користувача з події
        user = None
        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        
        if not user:
            return await handler(event, data)
        
        # Перевірити статус бану в базі
        try:
            async with aiosqlite.connect(DB_FILE) as db:
                cursor = await db.execute(
                    "SELECT is_banned FROM users WHERE telegram_id = ?",
                    (user.id,)
                )
                result = await cursor.fetchone()
                
                if result and result[0] == 1:
                    # Користувач заблокований
                    logger.info(f"Blocked access attempt from banned user {user.id}")
                    
                    # Відправити повідомлення про блокування
                    if event.message:
                        await event.message.answer(
                            "🚫 <b>Ваш акаунт заблокований</b>\n\n"
                            "Ви не можете використовувати бота.\n"
                            "Для отримання додаткової інформації зверніться до адміністрації."
                        )
                    elif event.callback_query:
                        await event.callback_query.answer(
                            "🚫 Ваш акаунт заблокований",
                            show_alert=True
                        )
                    
                    # Не виконувати handler
                    return
                    
        except Exception as e:
            logger.error(f"Error checking ban status for user {user.id}: {e}")
        
        # Користувач не заблокований, продовжити обробку
        return await handler(event, data)