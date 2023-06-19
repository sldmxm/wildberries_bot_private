from telegram import Update

from botmanager.models import TelegramUser


async def write_user(update: Update):
    """Запись данных пользователя в БД заявок."""
    await TelegramUser(
        username=update.effective_chat.username,
        first_name=update.effective_chat.first_name,
        telegram_id=update.effective_chat.id,
    ).asave()
