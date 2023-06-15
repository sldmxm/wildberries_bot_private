import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.text import MEMBER_STATUSES

load_dotenv()

CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')


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
        chat_id=CHANNEL_USERNAME,
        user_id=update.callback_query.from_user.id)
    if member.status in MEMBER_STATUSES:
        return True
    return False
