from datetime import datetime, timedelta

from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, ContextTypes

from .models import Destination, Job, ProductPosition
from .position_parser import get_position, get_result_text
from bot.constants import callback, text


async def create_job(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        article: int,
        query: str,
        interval: timedelta,
        start_time: datetime = None
) -> None:
    """Создание задачи для подписки на парсинг"""
    if start_time is None:
        start_time = datetime.now()
    user_id = update.effective_chat.id
    db_job = await Job.objects.filter(
        article=article,
        query=query,
        user_id=user_id
    ).afirst()
    if db_job is None:
        db_job = await Job.objects.acreate(
            article=article,
            query=query,
            user_id=user_id,
            interval=interval,
            start_time=start_time
        )
    elif interval != db_job.interval:
        db_job.interval = interval
    elif db_job.finished:
        db_job.finished = False
    else:
        return
    await db_job.asave()

    context.job_queue.run_repeating(
        schedule_parse,
        first=db_job.start_time,
        interval=interval,
        user_id=update.effective_chat.id,
        name=str(db_job.pk),
        data=db_job,
    )


async def schedule_parse(context: CallbackContext) -> None:
    """Регулярный парсинг по подписке"""
    article = context.job.data.article
    query = context.job.data.query
    results = await get_position(article, query)
    async for destination in Destination.objects.all():
        prev_result = await ProductPosition.objects.filter(
            job=context.job.data,
            destination=destination
        ).alast()
        if prev_result and destination.index in results:
            results[destination.index][
                'prev_position'
            ] = prev_result.total_position
        result = results.get(destination.index, {})
        page = result.get('page', None)
        position = result.get('position', None)
        await ProductPosition.objects.acreate(
            job=context.job.data,
            page=page,
            position=position,
            destination=destination
        )
    results_text = await get_result_text(results)
    response_text = text.PARSER_MESSAGE.format(
        article=article,
        query=query,
        result=results_text
    )
    keyboard = [
        [
            InlineKeyboardButton(
                'Отписаться',
                callback_data=callback.CALLBACK_UNSUBSCRIBE.format(
                    job_id=context.job.data.pk
                )
            ),
        ],
        [
            InlineKeyboardButton(
                'Выгрузить результаты в excel',
                callback_data=callback.CALLBACK_EXPORT_RESULTS.format(
                    job_id=context.job.data.pk
                )
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        context.job.user_id,
        text=response_text,
        reply_markup=reply_markup
    )


def start_jobs(application: Application) -> None:
    """автоматический старт подписок на парснг"""
    for db_job in Job.objects.filter(finished=False).all():
        application.job_queue.run_repeating(
            schedule_parse,
            first=db_job.start_time,
            interval=db_job.interval,
            user_id=db_job.user_id,
            name=str(db_job.pk),
            data=db_job
        )


async def stop_job(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        job_id: int
) -> None:
    """остановка подписки на парснг"""
    job = context.job_queue.get_jobs_by_name(str(job_id))
    if job:
        job[0].schedule_removal()
        db_job = await Job.objects.aget(pk=job_id)
        db_job.finished = True
        await db_job.asave()


@sync_to_async
def get_user_jobs(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> list[Job]:
    """получение подписок на парснг пользователя"""
    return list(Job.objects.filter(
        user_id=update.effective_chat.id,
        finished=False
    ).all())


@sync_to_async
def get_job_results(
        job_id: int
) -> list[ProductPosition]:
    """Получение результатов работы парсера"""
    return list(Job.objects.get(pk=job_id).productposition.all())
