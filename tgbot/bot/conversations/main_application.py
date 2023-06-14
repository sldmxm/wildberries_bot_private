import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from bot.constants.text import START_MESSAGE
from bot.core.settings import settings


TELEGRAM_TOKEN = settings.telegram_token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE)


def main():
    """Запуск бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    application.run_polling()
