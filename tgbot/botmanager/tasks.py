from time import sleep

from asgiref.sync import async_to_sync
from celery import shared_task
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from .models import Mailing
from bot.constants import text
from bot.core.logging import logger
from bot.core.settings import settings


@async_to_sync
async def send_messages(bot, user_id, message):
    """Конвертер для асинхронной отправки текстового сообщения."""
    async with bot:
        await bot.send_message(user_id, message, parse_mode=ParseMode.HTML)


@async_to_sync
async def send_photo(bot, user_id, photo):
    """Конвертер для асинхронной отправки фото."""
    if photo is not None:
        photo.seek(0, 0)
        async with bot:
            await bot.send_photo(user_id, photo)


@async_to_sync
async def send_document(bot, user_id, document):
    """Конвертер для асинхронной отправки файла."""
    if document is not None:
        document.seek(0, 0)
        async with bot:
            await bot.send_document(user_id, document, write_timeout=10)


@shared_task(bind=True)
def schedule_send_message(self, object_id):
    logger.info(text.LOG_MESSAGE_START_MAILING.format(mailing_id=object_id))
    bot = Bot(token=settings.telegram_token)
    message = Mailing.objects.get(pk=object_id)
    if message.image:
        byte_file_image = open(str(message.image), 'rb')
    else:
        byte_file_image = None
    if message.file_attache:
        byte_file_doc = open(str(message.file_attache), 'rb')
    else:
        byte_file_doc = None
    message_text = message.content
    if message.link:
        message_text += '\n' + message.link
    for recipient in message.recipients.all():
        try:
            send_photo(bot, recipient.telegram_id, byte_file_image)
            send_messages(bot, recipient.telegram_id, message_text)
            send_document(bot, recipient.telegram_id, byte_file_doc)
        except TelegramError as error:
            logger.error(
                text.LOG_MESSAGE_MAILING_ERROR.format(
                    user_id=recipient.telegram_id,
                    error=error.message
                ))
            if error.message.startswith('Can\'t parse entities'):
                return False
        sleep(0.2)
    logger.info(text.LOG_MESSAGE_STOP_MAILING.format(mailing_id=object_id))
    return True
