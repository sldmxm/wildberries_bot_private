import re
from parser.jobs import create_job, get_user_jobs, stop_job
from parser.position_parser import get_position, get_result_text
from parser.residue_parser import get_residue
from bot.core.logging import logger

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.callback import (
    CALLBACK_SCHEDULE_PARSER_PATTERN,
    CALLBACK_UNSUBSCRIBE_PATTERN,
    CALLBACK_UPDATE_PATTERN,
)
from bot.constants.text import (
    ACCEPTANCE_RATE_START_MESSAGE,
    CANCEL_MESSAGE,
    ERROR_MESSAGE,
    HELP_MESSAGE,
    LOG_MESSAGE_USER_START_PARSING,
    LOG_MESSAGE_DOWNLOAD,
    LOG_MESSAGE_RESIDUE_REQUEST,
    LOG_MESSAGE_UNSUBSCRIBE,
    LOG_MESSAGE_USER_SIGNED_UP,
    LOG_MESSAGE_USER_SUBSCRIPTION_CREATED,
    LOG_MESSAGE_USER_UPDATE_PARSING,
    LOG_MESSAGE_WRONG_ARTICLE,
    NO_SUBSCRIPTIONS_MESSAGE,
    PARSER_MESSAGE,
    PARSING_START_MESSAGE,
    PARSING_WAIT_MESSAGE,
    POSITION_PARSER_PATTERN,
    RESIDUE_PARSER_COUNT,
    RESIDUE_PARSER_MESSAGE,
    RESIDUE_PARSER_PATTERN,
    RESIDUE_PARSER_START_MESSAGE,
    SUBSCRIBE_MESSAGE,
    SUBSCRIPTIONS_MESSAGE,
    UNSUBSCRIBE_MESSAGE,
)
from bot.keyboards import (
    cancel_keyboard,
    menu_keyboard,
    position_parse_keyboard,
)
from bot.models import Callback
from bot.utils import check_subscription, write_user


(
    POSITION_PARSER_CONVERSATION,
    RESIDUE_PARSER_CONVERSATION,
    ACCEPTANCE_RATE_CONVERSATION
) = range(3)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню"""
    query = update.callback_query
    if await check_subscription(update, context):
        logger.info(LOG_MESSAGE_USER_SIGNED_UP.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id
            ))
        reply_markup = menu_keyboard()
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=HELP_MESSAGE,
            reply_markup=reply_markup
        )
        await write_user(update)
    else:
        await query.answer('Вы не подписались на канал.')


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
    reply_markup = cancel_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=PARSING_START_MESSAGE,
        reply_markup=reply_markup
    )
    return POSITION_PARSER_CONVERSATION


async def position_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера позиций"""
    match = re.match(POSITION_PARSER_PATTERN, update.message.text)
    logger.info(LOG_MESSAGE_USER_START_PARSING.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
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
        reply_markup = await position_parse_keyboard(article, query)
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
    logger.info(LOG_MESSAGE_WRONG_ARTICLE.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id))


async def update_position_parser(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка обновления позиции парсера"""
    match = re.match(CALLBACK_UPDATE_PATTERN, update.callback_query.data)
    logger.info(LOG_MESSAGE_USER_UPDATE_PARSING.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
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
    logger.info(LOG_MESSAGE_USER_SUBSCRIPTION_CREATED.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
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
    reply_markup = cancel_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=RESIDUE_PARSER_START_MESSAGE,
        reply_markup=reply_markup
    )
    return RESIDUE_PARSER_CONVERSATION


async def residue_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера остатков"""
    match = re.match(RESIDUE_PARSER_PATTERN, update.message.text)
    article = int(match.group(1))
    logger.info(LOG_MESSAGE_RESIDUE_REQUEST.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
    parser_data = await get_residue(article)
    if not parser_data:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ERROR_MESSAGE
        )
        return RESIDUE_PARSER_CONVERSATION
    residue_in_storehouses, residual_sizes = parser_data
    residue_in_storehouses_text = '\n'.join(
        [
            RESIDUE_PARSER_COUNT.format(name=city, count=count)
            for city, count in sorted(
                residue_in_storehouses.items(), key=lambda item: -item[1]
            )
        ]
    )
    residual_sizes_text = '\n'.join(
        [
            RESIDUE_PARSER_COUNT.format(name=size, count=count)
            for size, count in sorted(residual_sizes.items())
        ]
    )
    response_text = RESIDUE_PARSER_MESSAGE.format(
        residue_in_storehouses=residue_in_storehouses_text,
        residual_sizes=residual_sizes_text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )
    return RESIDUE_PARSER_CONVERSATION


async def acceptance_rate_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка вспомогательного сообщения коэффициента приемки"""
    reply_markup = cancel_keyboard()
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
    """Обработка выгрузки результатов"""
    logger.info(LOG_MESSAGE_DOWNLOAD.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id))
    pass


async def unsubscribe(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка отписки на позицию"""
    match = re.match(CALLBACK_UNSUBSCRIBE_PATTERN, update.callback_query.data)
    job_id = int(match.group(1))
    logger.info(LOG_MESSAGE_UNSUBSCRIBE.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=job_id))
    await stop_job(update=update, context=context, job_id=job_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=UNSUBSCRIBE_MESSAGE
    )
