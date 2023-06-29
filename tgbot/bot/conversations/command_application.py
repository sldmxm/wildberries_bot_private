from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes, ConversationHandler

from bot.constants.text import HELP_MESSAGE, START_MESSAGE, STOP_MESSAGE
from bot.keyboards import start_keyboard
from tgbot.settings import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    reply_markup = start_keyboard()
    logger.info(f'Пользователь с chat id {update.effective_chat.id} нажал кнопку start')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды help."""
    logger.info(f'Пользователь с chat id {update.effective_chat.id} нажал кнопку help')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stop."""
    logger.info(f'Пользователь с chat id {update.effective_chat.id} нажал кнопку stop')
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
