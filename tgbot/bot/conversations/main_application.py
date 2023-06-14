import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from bot.constants.text import (
    HELP_MESSAGE,
    START_MESSAGE,
    STOP_MESSAGE,
    SUBSCRIBTION_IS_FALSE,
    SUBSCRIBTION_IS_TRUE
)
from bot.utils import check_subscription


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""
    keyboard = [
                [
                    InlineKeyboardButton(
                        'Я подписался, запустить бота',
                        callback_data='Проверка подписки'
                    )
                ]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик выбора действий в кнопках под текстом."""
    query = update.callback_query
    await query.answer()
    if query.data == 'Проверка подписки':
        if await check_subscription(update, context):
            await update.effective_chat.send_message(SUBSCRIBTION_IS_TRUE)
        else:
            query = update.callback_query
            await query.answer()
            keyboard = [
                [
                    InlineKeyboardButton(
                        'Я подписался, запустить бота',
                        callback_data='Проверка подписки'
                    )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                SUBSCRIBTION_IS_FALSE,
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


def main():
    """Запуск бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('stop', stop))

    application.run_polling()
