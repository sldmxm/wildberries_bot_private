import logging
import os
from parser.jobs import start_jobs

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from .command_application import setup_my_commands
from bot.core.settings import settings
from bot.handlers import register_conversation_handlers


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    """Запуск бота."""
    application = (
        ApplicationBuilder().token(
            settings.telegram_token).post_init(setup_my_commands).build()
    )
    register_conversation_handlers(application)
    start_jobs(application)
    application.run_polling()
