from datetime import date, datetime, time, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callback import (
    CALLBACK_ACCEPTANCE_RATE,
    CALLBACK_CANCEL,
    CALLBACK_CHECK_SUBSCRIBE,
    CALLBACK_POSITION_PARSER,
    CALLBACK_RESIDUE_PARSER,
    CALLBACK_SCHEDULE_PARSER,
    CALLBACK_UPDATE,
    CALLBACK_USER_SUBSCRIPTIONS,
)
from bot.models import Callback


def start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Я подписался, запустить бота',
                callback_data=CALLBACK_CHECK_SUBSCRIBE
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def menu_keyboard():
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
    return InlineKeyboardMarkup(keyboard)


def cancel_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=CALLBACK_CANCEL
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
            interval=timedelta(seconds=hours),
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
                '12 часов',
                callback_data=CALLBACK_SCHEDULE_PARSER.format(
                    callback_id=callback_hourly[12].pk
                )
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
