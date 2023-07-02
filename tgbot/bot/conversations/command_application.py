from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, ConversationHandler

from bot.constants import text
from bot.keyboards import start_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    reply_markup = start_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.START_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды help."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.HELP_MESSAGE)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stop."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.STOP_MESSAGE)
    return ConversationHandler.END


async def setup_my_commands(application: Application):
    """Меню со списком команд"""
    bot_commands = [
        ('start', 'Запуск бота'),
        ('help', 'Получить инструкцию'),
        ('stop', 'Остановить бота'),
    ]
    await application.bot.set_my_commands(bot_commands)
