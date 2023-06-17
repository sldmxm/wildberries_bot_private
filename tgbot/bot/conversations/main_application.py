import logging
import os
from parser.jobs import start_jobs

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .menu_application import (
    ACCEPTANCE_RATE_CONVERSATION,
    POSITION_PARSER_CONVERSATION,
    RESIDUE_PARSER_CONVERSATION,
    acceptance_rate,
    acceptance_rate_help_message,
    callback_subscribe_position_parser,
    cancel,
    export_results,
    menu,
    position_parser,
    position_parser_help_message,
    residue_parser,
    residue_parser_help_message,
    unsubscribe,
    update_position_parser,
    user_subscriptions,
)
from bot.constants.callback import (
    CALLBACK_ACCEPTANCE_RATE,
    CALLBACK_CANCEL,
    CALLBACK_CHECK_SUBSCRIBE,
    CALLBACK_EXPORT_RESULTS_PATTERN,
    CALLBACK_POSITION_PARSER,
    CALLBACK_RESIDUE_PARSER,
    CALLBACK_SCHEDULE_PARSER_PATTERN,
    CALLBACK_UNSUBSCRIBE_PATTERN,
    CALLBACK_UPDATE_PATTERN,
    CALLBACK_USER_SUBSCRIPTIONS,
)
from bot.constants.text import START_MESSAGE


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
                callback_data=CALLBACK_CHECK_SUBSCRIBE
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=START_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


def register_conversation_handlers(application: Application) -> None:
    """Добавление обработчиков сообщений"""
    application.add_handler(
        CallbackQueryHandler(
            menu,
            pattern=CALLBACK_CHECK_SUBSCRIBE
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            unsubscribe,
            pattern=CALLBACK_UNSUBSCRIBE_PATTERN
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            export_results,
            pattern=CALLBACK_EXPORT_RESULTS_PATTERN
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            user_subscriptions,
            pattern=CALLBACK_USER_SUBSCRIPTIONS
        )
    )

    position_parser_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                position_parser_help_message,
                pattern=CALLBACK_POSITION_PARSER
            )
        ],
        states={
            POSITION_PARSER_CONVERSATION: [
                MessageHandler(
                    filters.Text(),
                    position_parser
                ),
                CallbackQueryHandler(
                    update_position_parser,
                    pattern=CALLBACK_UPDATE_PATTERN
                ),
                CallbackQueryHandler(
                    callback_subscribe_position_parser,
                    pattern=CALLBACK_SCHEDULE_PARSER_PATTERN
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel,
                pattern=CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(position_parser_conversation)

    residue_parser_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                residue_parser_help_message,
                pattern=CALLBACK_RESIDUE_PARSER
            )
        ],
        states={
            RESIDUE_PARSER_CONVERSATION: [
                MessageHandler(
                    filters.Text(),
                    residue_parser
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel,
                pattern=CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(residue_parser_conversation)

    acceptance_rate_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                acceptance_rate_help_message,
                pattern=CALLBACK_ACCEPTANCE_RATE
            )
        ],
        states={
            ACCEPTANCE_RATE_CONVERSATION: [
                MessageHandler(
                    filters.Text(),
                    acceptance_rate
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                cancel,
                pattern=CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(acceptance_rate_conversation)


def main():
    """Запуск бота."""
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    register_conversation_handlers(application)
    start_jobs(application)
    application.run_polling()
