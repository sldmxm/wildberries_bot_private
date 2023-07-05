from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.constants import callback, text
from bot.conversations import command_application, menu_application


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
            menu_application.cancel,
            pattern=callback.CALLBACK_CANCEL
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
    application.add_handler(
        CallbackQueryHandler(
            menu_application.position_parser_help_message,
            pattern=callback.CALLBACK_POSITION_PARSER
        )
    )
    application.add_handler(
        MessageHandler(
            filters.Regex(text.POSITION_PARSER_PATTERN),
            menu_application.position_parser
        ),
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.update_position_parser,
            pattern=callback.CALLBACK_UPDATE_PATTERN
        ),
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.callback_subscribe_position_parser,
            pattern=callback.CALLBACK_SCHEDULE_PARSER_PATTERN
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.residue_parser_help_message,
            pattern=callback.CALLBACK_RESIDUE_PARSER
        )
    )
    application.add_handler(
        MessageHandler(
            filters.Regex(text.RESIDUE_PARSER_PATTERN),
            menu_application.residue_parser
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.storehouses_page_1,
            pattern=callback.CALLBACK_ACCEPTANCE_RATE_HELP
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.acceptance_rate,
            pattern=callback.CALLBACK_STOREHOUSE_PATTERN
        ),
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.storehouses_page_1,
            pattern=callback.CALLBACK_SH_PAGE_1
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.storehouses_page_2,
            pattern=callback.CALLBACK_SH_PAGE_2
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_application.storehouses_page_3,
            pattern=callback.CALLBACK_SH_PAGE_3
        )
    )
