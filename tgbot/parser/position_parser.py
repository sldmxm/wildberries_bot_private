import asyncio
import json
from itertools import chain
from math import ceil

from .clientsession import ClientSession
from .constants import (
    ADVERT_PRODUCTS_LINK,
    PAGE_PARSING_LINK,
    TOTAL_PRODUCTS_LINK,
)
from .models import Destination
from bot.constants.text import (
    ADVERT_PRODUCT_POSITION_MESSAGE,
    PRODUCT_POSITION_MESSAGE,
    PRODUCT_POSITION_NOT_FOUND_MESSAGE,
    PRODUCT_POSITION_SCHEDULE_MESSAGE,
)


loop = asyncio.get_event_loop()


async def get_advert_position(article: int, query: str) -> int:
    """Проверка, является ли товар реклманым,
    если реклмнаый - возврщает его пзицию, иначе -1"""
    link = ADVERT_PRODUCTS_LINK.format(query=query)
    async with ClientSession() as session:
        response_data = await session.get_data(link)
    response_json = json.loads(response_data)
    adverts = response_json.get('adverts', [])
    pages = response_json.get('pages', [])
    if adverts is None or pages is None:
        return -1
    positions = [[
        position + 100 * page_index for position in page.get('positions', [])
    ] for page_index, page in enumerate(pages)]
    positions = list(chain(*positions))
    for index, advert in enumerate(adverts):
        if article == advert.get('id', None):
            return positions[index]
    return -1


async def get_total_positions(query: str, destination: int) -> int:
    """получение общего количества товаров по запросу"""
    link = TOTAL_PRODUCTS_LINK.format(query=query, destination=destination)
    async with ClientSession() as session:
        response_data = await session.get_data(link)
    response_json = json.loads(response_data)
    data = response_json.get('data', {})
    return data.get('total', 0)


async def parse_page(
        page: int,
        query: str,
        article: int,
        destination: int,
        tasks: list[asyncio.Task],
        result: dict
) -> None:
    """парсинг страниц с товаром"""
    link = PAGE_PARSING_LINK.format(
        destination=destination,
        page=str(page),
        query=query
    )
    async with ClientSession() as session:
        data = await session.get_data(link)
    response_json = json.loads(data)
    response_data = response_json.get('data', {})
    response_products = response_data.get('products', [])
    for index, product in enumerate(response_products):
        if product.get('id', None) == article:
            result[destination] = {
                'page': page,
                'position': index + 1
            }
            for task in tasks:
                task.cancel()


async def async_execute(
        query: str,
        article: int,
        destinations: list[int]
) -> dict:
    """Получение словаря с позицией товара в пункте выдачи заказа"""
    advert_position = await get_advert_position(article, query)
    if advert_position != -1:
        result = {
            destination: {
                'page': advert_position // 100 + 1,
                'position': advert_position % 100,
                'is_advert': True
            } for destination in destinations
        }
        return result
    result = {destination: {} for destination in destinations}
    tasks = []
    for destination in destinations:
        total_positions = await get_total_positions(query, destination)
        page_tasks = []
        for page in range(1, min(ceil(total_positions / 100), 61)):
            task = asyncio.ensure_future(parse_page(
                page,
                query,
                article,
                destination,
                page_tasks,
                result,
            ))
            page_tasks.append(task)
        tasks.append(page_tasks)
    tasks = list(chain(*tasks))
    if tasks:
        await asyncio.wait(tasks)
    return result


async def get_result_text(results: dict) -> str:
    """создание текстового сообщения с положением товаров"""
    is_advert = list(results.values())[0].get('is_advert', False)
    if is_advert:
        result_text = ADVERT_PRODUCT_POSITION_MESSAGE
    else:
        result_text = ''
    async for destination in Destination.objects.all():
        result = results.get(destination.index, {})
        page = result.get('page', None)
        position = result.get('position', None)
        prev_position = result.get('prev_position', None)
        if position is None or page is None:
            result_text += PRODUCT_POSITION_NOT_FOUND_MESSAGE.format(
                city=destination.city
            )
            continue
        total_position = (page - 1) * 100 + position
        if prev_position is None:
            result_text += PRODUCT_POSITION_MESSAGE.format(
                city=destination.city,
                position=total_position
            )
        else:
            if total_position > prev_position:
                position_arrow = ' ⬆'
            elif total_position == prev_position:
                position_arrow = ' ︎▬'
            else:
                position_arrow = ' ⬇'
            result_text += PRODUCT_POSITION_SCHEDULE_MESSAGE.format(
                city=destination.city,
                position=total_position,
                prev_position=prev_position,
                position_difference=abs(prev_position - total_position),
                position_arrow=position_arrow
            )
    return result_text


async def get_position(product_id: int, query: str) -> dict:
    """Получение словаря с позицией товара по всем пунктам выдачи заказа"""
    query = '%20'.join(query.split(' '))
    destinations = []
    async for destination in Destination.objects.all():
        destinations.append(destination.index)
    return await async_execute(
        query,
        product_id,
        destinations
    )
