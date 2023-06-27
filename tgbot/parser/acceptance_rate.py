import json
from http import HTTPStatus

import aiohttp
from prettytable import PrettyTable
from asgiref.sync import sync_to_async

from parser.models import Storehouse
from parser.constants import (
    ACCEPTANCE_HEADERS,
    ACCEPTANCE_LINK,
    PACKAGE,
)


def coef_in_text(coef: int) -> str:
    """Перевод полученного коэффициента в текст для таблицы"""
    if coef == 0:
        return 'Бесплатно'
    if not coef:
        return '-'
    if coef == -1:
        return 'Недоступно'
    return f'Платно x{coef}'


@sync_to_async
def get_sh_index(storehouse: str) -> int:
    """Получение индекса склада из базы"""
    return Storehouse.objects.get(name=storehouse).index


async def get_rates(storehouse: str) -> str:
    """
    Парсер данных о коэффициентах приемки  склада.
    Возвращение полученной информации в виде таблицы
    """
    sh_index = await get_sh_index(storehouse)
    table = PrettyTable()
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            ACCEPTANCE_LINK.format(index=sh_index),
            headers=ACCEPTANCE_HEADERS
        )
        if response.status != HTTPStatus.OK:
            return
        response_text = await response.text()
        response_json = json.loads(response_text)
        dates = ['Дата', ['-' for i in range(10)]]
        all_rates = []
        for key in response_json:
            rates = [PACKAGE[key], []]
            if len(response_json[key]) > 1:
                for i in range(10):
                    rates[1].append(coef_in_text(
                        response_json[key][i]['coefficient']
                        )
                    )
                    if dates[1][i] == '-':
                        dates[1][i] = response_json[key][i]['date'][:10]
            else:
                rates[1].extend(['-' for i in range(10)])
            all_rates.append(rates)
        table.add_column(*dates)
        for rate in all_rates:
            table.add_column(*rate)
        return table
