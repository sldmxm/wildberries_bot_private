from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants import callback, text
from bot.conversations import menu_application, command_application


def register_conversation_handlers(application: Application) -> None:
    """Добавление обработчиков сообщений"""
    application.add_handler(CommandHandler('start', command_application.start))
    application.add_handler(CommandHandler('help', command_application.help))
    application.add_handler(CommandHandler('stop', command_application.stop))

    application.add_handler(
        CallbackQueryHandler(
            menu_application.menu,
            pattern=callback.CALLBACK_CHECK_SUBSCRIBE
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.unsubscribe,
            pattern=callback.CALLBACK_UNSUBSCRIBE_PATTERN
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.export_results,
            pattern=callback.CALLBACK_EXPORT_RESULTS_PATTERN
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.user_subscriptions,
            pattern=callback.CALLBACK_USER_SUBSCRIPTIONS
        )
    )
    position_parser_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                menu_application.position_parser_help_message,
                pattern=callback.CALLBACK_POSITION_PARSER
            )
        ],
        states={
            menu_application.POSITION_PARSER_CONVERSATION: [
                MessageHandler(
                    filters.Regex(text.POSITION_PARSER_PATTERN),
                    menu_application.position_parser
                ),
                CallbackQueryHandler(
                    menu_application.update_position_parser,
                    pattern=callback.CALLBACK_UPDATE_PATTERN
                ),
                CallbackQueryHandler(
                    menu_application.callback_subscribe_position_parser,
                    pattern=callback.CALLBACK_SCHEDULE_PARSER_PATTERN
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                menu_application.cancel,
                pattern=callback.CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(position_parser_conversation)

    residue_parser_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                menu_application.residue_parser_help_message,
                pattern=callback.CALLBACK_RESIDUE_PARSER
            )
        ],
        states={
            menu_application.RESIDUE_PARSER_CONVERSATION: [
                MessageHandler(
                    filters.Regex(text.RESIDUE_PARSER_PATTERN),
                    menu_application.residue_parser
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                menu_application.cancel,
                pattern=callback.CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(residue_parser_conversation)

    acceptance_rate_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                menu_application.acceptance_rate_help_message,
                pattern=callback.CALLBACK_ACCEPTANCE_RATE
            )
        ],
        states={
            menu_application.ACCEPTANCE_RATE_CONVERSATION: [
                MessageHandler(
                    filters.Text(),
                    menu_application.acceptance_rate
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                menu_application.cancel,
                pattern=callback.CALLBACK_CANCEL
            )
        ],

    )
    application.add_handler(acceptance_rate_conversation)
