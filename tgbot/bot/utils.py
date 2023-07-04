from datetime import datetime, timedelta
from functools import wraps
from parser.models import Job, ProductPosition

from asgiref.sync import sync_to_async
from openpyxl import Workbook
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.text import MEMBER_STATUSES, NOT_SUBSCRIBED
from bot.core.settings import settings
from bot.models import UserAction
from botmanager.models import TelegramUser


REPORT_DAYS = 3


def check_user_subscription(func):
    """Декоратор проверки подписки на пользователя"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if await check_subscription(*args):
            return await func(*args, **kwargs)
        update, context = args
        query = update.callback_query
        if query is None:
            return await update.bot.send_message(
                chat_id=update.effective_chat.id,
                text=NOT_SUBSCRIBED,
            )
        return await query.answer(NOT_SUBSCRIBED)
    return wrapper


def register_user_action(action):
    """Декоратор для записи действия пользователя в базу данных"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            telegram_id = args[0].effective_chat.id
            await write_user(args[0])
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


@sync_to_async
def write_user(update: Update):
    """Запись данных пользователя в БД заявок."""
    if not TelegramUser.objects.filter(
        telegram_id=update.effective_chat.id
    ).exists():
        TelegramUser(
            username=update.effective_chat.username,
            first_name=update.effective_chat.first_name,
            telegram_id=update.effective_chat.id,
        ).save()


async def check_subscription(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Функция проверяет наличие подписки у пользователя на выбранную группу.
    Для того, чтобы проверка сработала нужно добавить бота в администраторы
    выбранной группы.
    """
    if update.callback_query is None:
        user_id = update.effective_chat.id
    else:
        user_id = update.callback_query.from_user.id
    member = await context.bot.get_chat_member(
        chat_id=settings.channel_username,
        user_id=user_id)
    if member.status in MEMBER_STATUSES:
        return True
    return False


@sync_to_async
def data_export_to_xls(
    job_id: int
) -> str:
    """Функция сохраняет данные последнего отчета по подписке парсера выбранной
    позиций в Excel файл и возвращает его имя.
    """
    wb = Workbook()
    ws = wb.active
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['D'].width = 25
    job = Job.objects.get(pk=job_id)
    article = job.article
    query = job.query
    product_positions = list(ProductPosition.objects.filter(
        job=job_id,
        datetime__range=[
            datetime.now() - timedelta(days=REPORT_DAYS), datetime.now()
        ]
    ))
    filename = f'{article}.xlsx'
    data = [
        ['Артикул:', str(article), 'Запроc:', query],
        ['', '', '', ''],
        ['Место', 'Позиция', 'Cтраница', 'Дата и время отчета']
    ]

    for product_position in product_positions:
        data.append(
            [
                product_position.destination.city,
                product_position.position,
                product_position.page,
                product_position.datetime.strftime("%d.%m.%Y %H:%M")
            ]
        )

    for row in data:
        ws.append(row)

    wb.save(filename)
    return filename
