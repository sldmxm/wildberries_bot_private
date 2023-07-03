from datetime import date, datetime, time, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import callback
from bot.models import Callback


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
                callback_data=callback.CALLBACK_ACCEPTANCE_RATE_HELP
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


def storehouses_keyboard_1():
    keyboard = [
        [
            InlineKeyboardButton(
                'Екатеринбург',
                callback_data=callback.CALLBACK_SH_EKATERINBURG
            ),
            InlineKeyboardButton(
                'Коледино',
                callback_data=callback.CALLBACK_SH_KOLEDINO
            ),
        ],
        [
            InlineKeyboardButton(
                'Крёкшино КБТ',
                callback_data=callback.CALLBACK_SH_KREKSHINO_KBT
            ),
            InlineKeyboardButton(
                'Новосибирск',
                callback_data=callback.CALLBACK_SH_NOVOSIBIRSK
            ),
        ],
        [
            InlineKeyboardButton(
                'Санкт-Петербург',
                callback_data=callback.CALLBACK_SH_SAINT_PETERSBURG
            ),
            InlineKeyboardButton(
                'Казань',
                callback_data=callback.CALLBACK_SH_KAZAN
            ),
        ],
        [
            InlineKeyboardButton(
                'Краснодар',
                callback_data=callback.CALLBACK_SH_KRASNODAR
            ),
            InlineKeyboardButton(
                'Подольск',
                callback_data=callback.CALLBACK_SH_PODOLSK
            ),
        ],
        [
            InlineKeyboardButton(
                'Стр. 2',
                callback_data=callback.CALLBACK_SH_PAGE_2
            ),
            InlineKeyboardButton(
                'Стр. 3',
                callback_data=callback.CALLBACK_SH_PAGE_3
            ),
        ],
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=callback.CALLBACK_CANCEL
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def storehouses_keyboard_2():
    keyboard = [
        [
            InlineKeyboardButton(
                'Казахстан',
                callback_data=callback.CALLBACK_SH_KAZAKHSTAN
            ),
            InlineKeyboardButton(
                'Санкт-Петербург Шушары',
                callback_data=callback.CALLBACK_SH_SAINT_PETERSBURG_SHUSHARY
            ),
        ],
        [
            InlineKeyboardButton(
                'Белая Дача',
                callback_data=callback.CALLBACK_SH_BELAYA_DACHA
            ),
            InlineKeyboardButton(
                'Электросталь',
                callback_data=callback.CALLBACK_SH_ELEKTROSTAL
            ),
        ],
        [
            InlineKeyboardButton(
                'Электросталь КБТ',
                callback_data=callback.CALLBACK_SH_ELEKTROSTAL_KBT
            ),
            InlineKeyboardButton(
                'Тула',
                callback_data=callback.CALLBACK_SH_TULA
            ),
        ],
        [
            InlineKeyboardButton(
                'Чехов',
                callback_data=callback.CALLBACK_SH_CHEKHOV
            ),
            InlineKeyboardButton(
                'Домодедово',
                callback_data=callback.CALLBACK_SH_DOMODEDOVO
            ),
        ],
        [
            InlineKeyboardButton(
                'Стр. 1',
                callback_data=callback.CALLBACK_SH_PAGE_1
            ),
            InlineKeyboardButton(
                'Стр. 3',
                callback_data=callback.CALLBACK_SH_PAGE_3
            ),
        ],
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=callback.CALLBACK_CANCEL
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def storehouses_keyboard_3():
    keyboard = [
        [
            InlineKeyboardButton(
                'Невинномысск',
                callback_data=callback.CALLBACK_SH_NEVINNOMYSSK
            ),
            InlineKeyboardButton(
                'Чехов 2',
                callback_data=callback.CALLBACK_SH_CHEKHOV_2
            ),
        ],
        [
            InlineKeyboardButton(
                'Вёшки',
                callback_data=callback.CALLBACK_SH_VESHKI
            ),
            InlineKeyboardButton(
                'Минск',
                callback_data=callback.CALLBACK_SH_MINSK
            ),
        ],
        [
            InlineKeyboardButton(
                'Хабаровск',
                callback_data=callback.CALLBACK_SH_KHABAROVSK
            ),
            InlineKeyboardButton(
                'Пушкино',
                callback_data=callback.CALLBACK_SH_PUSHKINO
            ),
        ],
        [
            InlineKeyboardButton(
                'Обухово',
                callback_data=callback.CALLBACK_SH_OBUKHOVO
            ),
            InlineKeyboardButton(
                'Подольск 3',
                callback_data=callback.CALLBACK_SH_PODOLSK_3
            ),
        ],
        [
            InlineKeyboardButton(
                'Стр. 1',
                callback_data=callback.CALLBACK_SH_PAGE_1
            ),
            InlineKeyboardButton(
                'Стр. 2',
                callback_data=callback.CALLBACK_SH_PAGE_2
            ),
        ],
        [
            InlineKeyboardButton(
                'Отмена',
                callback_data=callback.CALLBACK_CANCEL
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def return_to_storehouse_page_1_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                'Вернуться к выбору склада',
                callback_data=callback.CALLBACK_SH_PAGE_1
            )
        ],
        [
            InlineKeyboardButton(
                'Вернуться в меню',
                callback_data=callback.CALLBACK_CANCEL
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
