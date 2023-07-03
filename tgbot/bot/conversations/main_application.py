from parser.jobs import start_jobs

from telegram.ext import ApplicationBuilder

from .command_application import setup_my_commands
from bot.core.settings import settings
from bot.handlers import register_conversation_handlers


def main():
    """Запуск бота."""
    application = (
        ApplicationBuilder().token(
            settings.telegram_token
        ).post_init(setup_my_commands).concurrent_updates(True).build()
    )
    register_conversation_handlers(application)
    start_jobs(application)
    if settings.webhook_url is None:
        application.run_polling()
    else:
        application.run_webhook(
            listen=settings.webhook_local_link,
            port=settings.webhook_port,
            webhook_url=settings.webhook_url
        )
