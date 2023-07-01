from datetime import date, datetime, time, timedelta

import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import callback
from bot.models import Callback
from tgbot import settings


def start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Я подписался, запустить бота',
                callback_data=callback.CALLBACK_CHECK_SUBSCRIBE
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Парсер позиций',
                callback_data=callback.CALLBACK_POSITION_PARSER
            ),
        ],
        [
            InlineKeyboardButton(
                'Парсер остатков',
                callback_data=callback.CALLBACK_RESIDUE_PARSER
            )
        ],
        [
            InlineKeyboardButton(
                'Отслеживание коэффициента приемки WB',
                callback_data=callback.CALLBACK_ACCEPTANCE_RATE
            )
        ],
        [
            InlineKeyboardButton(
                'Мои подписки на позиции',
                callback_data=callback.CALLBACK_USER_SUBSCRIPTIONS
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=callback.CALLBACK_CANCEL
            ),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def position_parse_keyboard(article: int, query: str):
    """Создание клавиатуры парсера позиций"""
    callback_update = await Callback.objects.acreate(
        article=article,
        query=query
    )
    timezone = pytz.timezone(settings.TIME_ZONE)
    nine_am = time(hour=9, tzinfo=timezone)
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
                callback_data=callback.CALLBACK_UPDATE.format(
                    callback_id=callback_update.pk
                )
            ),
        ],
        [
            InlineKeyboardButton(
                'Результаты в 9:00. Подписаться',
                callback_data=callback.CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_daily.pk
                )
            )
        ],
        [
            InlineKeyboardButton(
                '1 час',
                callback_data=callback.CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[1].pk
                )
            ),
            InlineKeyboardButton(
                '6 часов',
                callback_data=callback.CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[6].pk
                )
            ),
            InlineKeyboardButton(
                '12 часов',
                callback_data=callback.CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[12].pk
                )
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def schedule_parse_keyboard(job_id):
    keyboard = [
        [
            InlineKeyboardButton(
                'Отписаться',
                callback_data=callback.CALLBACK_UNSUBSCRIBE.format(
                    job_id=job_id
                )
            ),
        ],
        [
            InlineKeyboardButton(
                'Выгрузить результаты в excel',
                callback_data=callback.CALLBACK_EXPORT_RESULTS.format(
                    job_id=job_id
                )
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
