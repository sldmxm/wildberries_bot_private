from asgiref.sync import sync_to_async
from telegram import Update

from botmanager.models import TelegramUser


@sync_to_async
def write_user(update: Update):
    """Запись данных пользователя ТГ"""
    TelegramUser(
        username=update.effective_chat.username,
        first_name=update.effective_chat.first_name,
        telegram_id=update.effective_chat.id,
    ).save()
