import re
from datetime import date, datetime, time, timedelta
from parser.jobs import create_job, get_user_jobs, stop_job
from parser.position_parser import get_position, get_result_text

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.callback import (
    CALLBACK_ACCEPTANCE_RATE,
    CALLBACK_CANCEL,
    CALLBACK_POSITION_PARSER,
    CALLBACK_RESIDUE_PARSER,
    CALLBACK_SCHEDULE_PARSER,
    CALLBACK_SCHEDULE_PARSER_PATTERN,
    CALLBACK_UNSUBSCRIBE_PATTERN,
    CALLBACK_UPDATE,
    CALLBACK_UPDATE_PATTERN,
    CALLBACK_USER_SUBSCRIPTIONS,
)
from bot.constants.text import (
    ACCEPTANCE_RATE_START_MESSAGE,
    CANCEL_MESSAGE,
    HELP_MESSAGE,
    NO_SUBSCRIPTIONS_MESSAGE,
    PARSER_MESSAGE,
    PARSING_START_MESSAGE,
    PARSING_WAIT_MESSAGE,
    RESIDUE_PARSER_START_MESSAGE,
    SUBSCRIBE_MESSAGE,
    SUBSCRIPTIONS_MESSAGE,
    UNSUBSCRIBE_MESSAGE,
)
from bot.models import Callback


(
    POSITION_PARSER_CONVERSATION,
    RESIDUE_PARSER_CONVERSATION,
    ACCEPTANCE_RATE_CONVERSATION
) = range(3)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню"""
    keyboard = [
        [
            InlineKeyboardButton(
                'Парсер позиций',
                callback_data=CALLBACK_POSITION_PARSER
            ),
        ],
        [
            InlineKeyboardButton(
                'Парсер остатков',
                callback_data=CALLBACK_RESIDUE_PARSER
            )
        ],
        [
            InlineKeyboardButton(
                'Отслеживание коэффициента приемки WB',
                callback_data=CALLBACK_ACCEPTANCE_RATE
            )
        ],
        [
            InlineKeyboardButton(
                'Мои подписки на позиции',
                callback_data=CALLBACK_USER_SUBSCRIPTIONS
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_MESSAGE,
        reply_markup=reply_markup
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка отмены действия"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=CANCEL_MESSAGE
    )
    await menu(update, context)
    return ConversationHandler.END


async def position_parser_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """обработка вспомогательного сообщения парсера позиций"""
    keyboard = [
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=CALLBACK_CANCEL
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=PARSING_START_MESSAGE,
        reply_markup=reply_markup
    )
    return POSITION_PARSER_CONVERSATION


async def build_position_parse_keyboard(article: int, query: str):
    """Создание клавиатуры парсера позиций"""
    callback_update = await Callback.objects.acreate(
        article=article,
        query=query
    )
    nine_am = time(hour=9)
    current_date = date.today()
    start_time = datetime.combine(current_date, nine_am)
    callback_daily = await Callback.objects.acreate(
        article=article,
        query=query,
        interval=timedelta(days=1),
        start_time=start_time
    )
    callback_hourly = {
        hours: await Callback.objects.acreate(
            article=article,
            query=query,
            interval=timedelta(hours=hours),
        ) for hours in [1, 6, 12]
    }
    keyboard = [
        [
            InlineKeyboardButton(
                'Обновить',
                callback_data=CALLBACK_UPDATE.format(
                    callback_id=callback_update.pk
                )
            ),
        ],
        [
            InlineKeyboardButton(
                'Результаты в 9:00. Подписаться',
                callback_data=CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_daily.pk
                )
            )
        ],
        [
            InlineKeyboardButton(
                '1 час',
                callback_data=CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[1].pk
                )
            ),
            InlineKeyboardButton(
                '6 часов',
                callback_data=CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[6].pk
                )
            ),
            InlineKeyboardButton(
                '12 часос',
                callback_data=CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[12].pk
                )
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def position_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера позиций"""
    match = re.match(r'^(\d+)\s+(.+)$', update.message.text)
    response_text = "Invalid request"
    if match:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=PARSING_WAIT_MESSAGE
        )
        article = int(match.group(1))
        query = match.group(2)
        results = await get_position(article, query)
        results_text = await get_result_text(results)
        reply_markup = await build_position_parse_keyboard(article, query)
        response_text = PARSER_MESSAGE.format(
            article=article,
            query=query,
            result=results_text
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text,
            reply_markup=reply_markup
        )
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )


async def update_position_parser(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка обновления позиции парсера"""
    match = re.match(CALLBACK_UPDATE_PATTERN, update.callback_query.data)
    callback_id = int(match.group(1))
    callback_data = await Callback.objects.aget(pk=callback_id)
    results = await get_position(callback_data.article, callback_data.query)
    results_text = await get_result_text(results)
    response_text = PARSER_MESSAGE.format(
        article=callback_data.article,
        query=callback_data.query,
        result=results_text
    )
    if response_text != update.callback_query.message.text:
        await context.bot.answer_callback_query(update.callback_query.id,
                                                'Ничего не изменилось')
        return POSITION_PARSER_CONVERSATION
    await context.bot.edit_message_text(
        response_text,
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=update.callback_query.message.reply_markup
    )
    await context.bot.answer_callback_query(update.callback_query.id,
                                            'Обновлено')
    return POSITION_PARSER_CONVERSATION


async def callback_subscribe_position_parser(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка подписки на позицию парсера"""
    match = re.match(
        CALLBACK_SCHEDULE_PARSER_PATTERN,
        update.callback_query.data
    )
    callback_id = int(match.group(1))
    callback_data = await Callback.objects.aget(pk=callback_id)
    await create_job(
        update=update,
        context=context,
        article=callback_data.article,
        query=callback_data.query,
        interval=callback_data.interval,
        start_time=callback_data.start_time
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=SUBSCRIBE_MESSAGE
    )
    return POSITION_PARSER_CONVERSATION


async def residue_parser_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка вспомогательного сообщения парсера остатков"""
    keyboard = [
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=CALLBACK_CANCEL
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=RESIDUE_PARSER_START_MESSAGE,
        reply_markup=reply_markup
    )
    return RESIDUE_PARSER_CONVERSATION


async def residue_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера остатков"""
    await context.bot.answer_callback_query(
        update.callback_query.id,
        'В разработке'
    )
    return RESIDUE_PARSER_CONVERSATION


async def acceptance_rate_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка вспомогательного сообщения коэффициента приемки"""
    keyboard = [
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=CALLBACK_CANCEL
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ACCEPTANCE_RATE_START_MESSAGE,
        reply_markup=reply_markup
    )
    return ACCEPTANCE_RATE_CONVERSATION


async def acceptance_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка коэффициента приемки"""
    await context.bot.answer_callback_query(
        update.callback_query.id,
        'В разработке'
    )
    return ACCEPTANCE_RATE_CONVERSATION


async def user_subscriptions(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка подписок на позиции"""
    jobs = await get_user_jobs(update, context)
    if jobs:
        results = '\n'.join([f'{job.article} {job.query}' for job in jobs])
        response_text = SUBSCRIPTIONS_MESSAGE.format(results=results)
    else:
        response_text = NO_SUBSCRIPTIONS_MESSAGE
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )


async def export_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выгруски результатов"""
    ...


async def unsubscribe(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка отписки на позицию"""
    match = re.match(CALLBACK_UNSUBSCRIBE_PATTERN, update.callback_query.data)
    job_id = int(match.group(1))
    await stop_job(update=update, context=context, job_id=job_id)
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=UNSUBSCRIBE_MESSAGE
        )
