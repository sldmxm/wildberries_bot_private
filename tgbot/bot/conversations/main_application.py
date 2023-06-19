import logging

from telegram import Update
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.text import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from bot.core.settings import settings
from bot.handlers import button


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    keyboard = [
                [
                    Button(
                        'Я подписался, запустить бота',
                        callback_data='check_subscription'
                    )
                ]
            ]
    reply_markup = Keyboard(keyboard)
    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды help."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stop."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=STOP_MESSAGE)
    return ConversationHandler.END


async def setup_my_commands(application: Application):
    """Меню со списком команд"""
    bot_commands = [
        ('start', 'Запуск бота'),
        ('help', 'Получить инструкцию'),
        ('stop', 'Остановить бота'),
    ]
    await application.bot.set_my_commands(bot_commands)


def main():
    """Запуск бота."""
    application = (
        ApplicationBuilder().token(settings.telegram_token).
        post_init(setup_my_commands).build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('stop', stop))

    application.run_polling()
