import re
from parser.acceptance_rate import get_rates
from parser.jobs import create_job, get_user_jobs, stop_job
from parser.position_parser import get_position, get_result_text
from parser.residue_parser import get_residue

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import keyboards
from bot.constants import actions, callback, states, text
from bot.core.logging import logger
from bot.models import Callback
from bot.utils import (
    check_user_subscription,
    data_export_to_xls,
    register_user_action,
    write_user,
)


@check_user_subscription
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню"""
    reply_markup = keyboards.menu_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.HELP_MESSAGE,
        reply_markup=reply_markup
    )
    await write_user(update)


@check_user_subscription
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка отмены действия"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.CANCEL_MESSAGE
    )
    await menu(update, context)
    return ConversationHandler.END


@check_user_subscription
async def position_parser_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """обработка вспомогательного сообщения парсера позиций"""
    reply_markup = keyboards.cancel_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.PARSING_START_MESSAGE,
        reply_markup=reply_markup
    )
    return states.POSITION_PARSER_CONVERSATION


@check_user_subscription
@register_user_action(actions.POSITION_PARSER)
async def position_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера позиций"""
    match = re.match(text.POSITION_PARSER_PATTERN, update.message.text)
    logger.info(text.LOG_MESSAGE_USER_START_PARSING.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
    response_text = "Invalid request"
    if match:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text.PARSING_WAIT_MESSAGE
        )
        article = int(match.group(1))
        query = match.group(2)
        results = await get_position(article, query)
        results_text = await get_result_text(results)
        reply_markup = await keyboards.position_parse_keyboard(article, query)
        response_text = text.PARSER_MESSAGE.format(
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
    logger.info(text.LOG_MESSAGE_WRONG_ARTICLE.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id))


@check_user_subscription
@register_user_action(actions.UPDATE_POSITION)
async def update_position_parser(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка обновления позиции парсера"""
    match = re.match(
        callback.CALLBACK_UPDATE_PATTERN,
        update.callback_query.data
    )
    logger.info(text.LOG_MESSAGE_USER_UPDATE_PARSING.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
    callback_id = int(match.group(1))
    callback_data = await Callback.objects.aget(pk=callback_id)
    results = await get_position(callback_data.article, callback_data.query)
    results_text = await get_result_text(results)
    response_text = text.PARSER_MESSAGE.format(
        article=callback_data.article,
        query=callback_data.query,
        result=results_text
    )
    if response_text != update.callback_query.message.text:
        await context.bot.answer_callback_query(update.callback_query.id,
                                                'Ничего не изменилось')
        return states.POSITION_PARSER_CONVERSATION
    await context.bot.edit_message_text(
        response_text,
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=update.callback_query.message.reply_markup
    )
    await context.bot.answer_callback_query(update.callback_query.id,
                                            'Обновлено')
    return states.POSITION_PARSER_CONVERSATION


@check_user_subscription
@register_user_action(actions.SUBSCRIBE)
async def callback_subscribe_position_parser(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка подписки на позицию парсера"""
    match = re.match(
        callback.CALLBACK_SCHEDULE_PARSER_PATTERN,
        update.callback_query.data
    )
    callback_id = int(match.group(1))
    callback_data = await Callback.objects.aget(pk=callback_id)
    logger.info(text.LOG_MESSAGE_USER_SUBSCRIPTION_CREATED.format(
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
        text=text.SUBSCRIBE_MESSAGE
    )
    return states.POSITION_PARSER_CONVERSATION


@check_user_subscription
async def residue_parser_help_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка вспомогательного сообщения парсера остатков"""
    reply_markup = keyboards.cancel_keyboard()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.RESIDUE_PARSER_START_MESSAGE,
        reply_markup=reply_markup
    )
    return states.RESIDUE_PARSER_CONVERSATION


@check_user_subscription
async def residue_parser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка парсера остатков"""
    match = re.match(text.RESIDUE_PARSER_PATTERN, update.message.text)
    article = int(match.group(1))
    logger.info(text.LOG_MESSAGE_RESIDUE_REQUEST.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=int(match.group(1))))
    parser_data = await get_residue(article)
    if not parser_data:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text.ERROR_MESSAGE
        )
        return states.RESIDUE_PARSER_CONVERSATION
    residue_in_storehouses, residual_sizes = parser_data
    residue_in_storehouses_text = '\n'.join(
        [
            text.RESIDUE_PARSER_COUNT.format(name=city, count=count)
            for city, count in sorted(
                residue_in_storehouses.items(), key=lambda item: -item[1]
            )
        ]
    )
    residual_sizes_text = '\n'.join(
        [
            text.RESIDUE_PARSER_COUNT.format(name=size, count=count)
            for size, count in sorted(residual_sizes.items())
        ]
    )
    response_text = text.RESIDUE_PARSER_MESSAGE.format(
        residue_in_storehouses=residue_in_storehouses_text,
        residual_sizes=residual_sizes_text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )
    return states.RESIDUE_PARSER_CONVERSATION


@check_user_subscription
async def storehouses_page_1(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Первая страница с выбором складов"""
    reply_markup = keyboards.storehouses_keyboard_1()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.ACCEPTANCE_RATE_START_MESSAGE,
        reply_markup=reply_markup
    )
    return states.ACCEPTANCE_RATE_CONVERSATION


@check_user_subscription
async def storehouses_page_2(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Вторая страница с выбором складов"""
    reply_markup = keyboards.storehouses_keyboard_2()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.ACCEPTANCE_RATE_START_MESSAGE,
        reply_markup=reply_markup
    )
    return states.ACCEPTANCE_RATE_CONVERSATION


@check_user_subscription
async def storehouses_page_3(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Третья страница с выбором складов"""
    reply_markup = keyboards.storehouses_keyboard_3()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.ACCEPTANCE_RATE_START_MESSAGE,
        reply_markup=reply_markup
    )
    return states.ACCEPTANCE_RATE_CONVERSATION


@check_user_subscription
async def acceptance_rate(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """Обработка коэффициента приемки"""
    reply_markup = keyboards.return_to_storehouse_page_1_keyboard()
    storehouse = update.callback_query.data.split(':')[1]
    table = await get_rates(storehouse)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{storehouse}:\n<pre>{table}</pre>',
        parse_mode='HTML',
        reply_markup=reply_markup,
    )
    return states.ACCEPTANCE_RATE_CONVERSATION


@check_user_subscription
async def user_subscriptions(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка подписок на позиции"""
    jobs = await get_user_jobs(update, context)
    if jobs:
        results = '\n'.join([f'{job.article} {job.query}' for job in jobs])
        response_text = text.SUBSCRIPTIONS_MESSAGE.format(results=results)
    else:
        response_text = text.NO_SUBSCRIPTIONS_MESSAGE
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_text
    )


@check_user_subscription
async def export_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выгруски результатов"""
    match = re.match(
        callback.CALLBACK_EXPORT_RESULTS_PATTERN, update.callback_query.data
    )
    logger.info(text.LOG_MESSAGE_DOWNLOAD.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id))
    job_id = int(match.group(1))
    file = await data_export_to_xls(job_id=job_id)
    doc = open(file, 'rb')
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=doc
    )


async def unsubscribe(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """Обработка отписки на позицию"""
    match = re.match(
        callback.CALLBACK_UNSUBSCRIBE_PATTERN,
        update.callback_query.data
    )
    job_id = int(match.group(1))
    logger.info(text.LOG_MESSAGE_UNSUBSCRIBE.format(
                username=update.effective_chat.username,
                chat_id=update.effective_chat.id,
                position=job_id))
    await stop_job(update=update, context=context, job_id=job_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.UNSUBSCRIBE_MESSAGE
    )
