from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.text import MEMBER_STATUSES
from bot.core.settings import settings
from bot.models import UserAction
from botmanager.models import TelegramUser


async def write_user(update: Update):
    """Запись данных пользователя в БД заявок."""
    await TelegramUser(
        username=update.effective_chat.username,
        first_name=update.effective_chat.first_name,
        telegram_id=update.effective_chat.id,
    ).asave()


async def check_subscription(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Функция проверяет наличие подписки у пользователя на выбранную группу.
    Для того, чтобы проверка сработала нужно добавить бота в администраторы
    выбранной группы.
    """
    member = await context.bot.get_chat_member(
        chat_id=settings.channel_username,
        user_id=update.callback_query.from_user.id)
    if member.status in MEMBER_STATUSES:
        return True
    return False


def register_user_action(action):
    """Декоратор для записи действия пользователя в базу данных"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            telegram_id = args[0].effective_chat.id
            telegram_user = await TelegramUser.objects.aget(
                    telegram_id=telegram_id
                )
            user_action = await UserAction.objects.acreate(
                telegram_user=telegram_user,
                action=action
            )
            await func(*args, **kwargs)
            await user_action.asave()
        return wrapper
    return decorator
