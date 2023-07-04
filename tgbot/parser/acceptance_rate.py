import json
from parser.constants import ACCEPTANCE_HEADERS, ACCEPTANCE_LINK, PACKAGE
from parser.models import Storehouse

from asgiref.sync import sync_to_async
from prettytable import PrettyTable

from .clientsession import ClientSession


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
    link = ACCEPTANCE_LINK.format(index=sh_index)
    async with ClientSession(headers=ACCEPTANCE_HEADERS) as session:
        response_data = await session.get_data(link)
    response_json = json.loads(response_data)
    dates = ['Дата', ['-' for i in range(10)]]
    all_rates = []
    for key in response_json:
        rates = [PACKAGE[key], []]
        if len(response_json[key]) > 1:
            for i in range(10):
                rates[1].append(coef_in_text(
                    response_json[key][i]['coefficient']
                ))
                if dates[1][i] == '-':
                    dates[1][i] = response_json[key][i]['date'][:10]
        else:
            rates[1].extend(['-' for i in range(10)])
        all_rates.append(rates)
    table.add_column(*dates)
    for rate in all_rates:
        table.add_column(*rate)
    return table
