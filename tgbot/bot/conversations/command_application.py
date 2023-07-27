from parser.jobs import get_user_jobs, stop_job

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, ContextTypes

from bot.conversations import menu_application
from bot.keyboards import start_keyboard
from bot.utils import get_text_for_ui_control
from bot.constants import text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    reply_markup = start_keyboard()
    target_text = get_text_for_ui_control(
        'start_message') or text.START_MESSAGE

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=target_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды help."""
    target_text = get_text_for_ui_control(
        'help_message') or text.HELP_MESSAGE
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=target_text)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stop."""
    target_text = get_text_for_ui_control(
        'stop_message') or text.STOP_MESSAGE
    user_jobs = await get_user_jobs(update, context)
    for user_job in user_jobs:
        await stop_job(update, context, user_job.pk)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=target_text)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stop."""
    await menu_application.menu(update, context)


async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды position."""
    await menu_application.position_parser_help_message(update, context)


async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды stock."""
    await menu_application.residue_parser_help_message(update, context)


async def storehouse_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды storehouse_rate."""
    await menu_application.storehouses_page_1(update, context)


async def my_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды my_subscriptions."""
    await menu_application.user_subscriptions(update, context)


async def setup_my_commands(application: Application):
    """Меню со списком команд"""
    bot_commands = [
        ('start', 'Запуск бота'),
        ('help', 'Получить инструкцию'),
        ('stop', 'Остановить бота'),
        ('menu', 'Главное меню'),
        ('position', 'Парсер позиций'),
        ('stock', 'Парсер остатков'),
        ('storehouse_rate', 'Отслеживание коэффициента приемки WB'),
        ('my_subscriptions', 'Мои подписки на позиции'),
    ]
    await application.bot.set_my_commands(bot_commands)
