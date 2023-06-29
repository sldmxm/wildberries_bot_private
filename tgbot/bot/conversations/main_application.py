from telegram.ext import ApplicationBuilder
from tgbot.settings import logger

from .command_application import setup_my_commands
from bot.core.settings import settings
from bot.handlers import register_conversation_handlers
from parser.jobs import start_jobs


def main():
    """Запуск бота."""
    application = (
        ApplicationBuilder().token(
            settings.telegram_token
        ).post_init(setup_my_commands).concurrent_updates(True).build()
    )
    register_conversation_handlers(application)
    start_jobs(application)
    application.run_polling()
    logger.info('Бот запущен')
