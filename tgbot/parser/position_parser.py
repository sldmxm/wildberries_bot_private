import asyncio
from http import HTTPStatus
from itertools import chain
from math import ceil

import aiohttp

from .constants import PAGE_PARSING_LINK, TOTAL_PRODUCTS_LINK
from .models import Destination
from bot.constants.text import (
    PRODUCT_POSITION_MESSAGE,
    PRODUCT_POSITION_NOT_FOUND_MESSAGE,
    PRODUCT_POSITION_SCHEDULE_MESSAGE,
)
import json
from .clientsession import ClientSession

loop = asyncio.get_event_loop()


async def get_total_positions(query: str, destination: int) -> int:
    """получение общего количества товаров по запросу"""
    link = TOTAL_PRODUCTS_LINK.format(query=query, destination=destination)
    async with ClientSession() as session:
        try:
            async with session.get(link, timeout=10) as response:
                if response.status != HTTPStatus.OK:
                    return await get_total_positions(query, destination)
                data = await response.content.read()
        except TimeoutError:
            return await get_total_positions(query, destination)
        response_json = json.loads(data)
        response_data = response_json.get('data', {})
        return response_data.get('total', 0)


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
        try:
            async with session.get(link, timeout=5) as response:
                if response.status != HTTPStatus.OK:
                    return await parse_page(
                        page,
                        query,
                        article,
                        destination,
                        tasks,
                        result
                    )
                data = await response.content.read()
        except TimeoutError:
            return await parse_page(
                page,
                query,
                article,
                destination,
                tasks,
                result
            )
        response_json = json.loads(data)
        response_data = response_json.get('data', {})
        response_products = response_data.get('products', [])
        article_list = [product.get('id', None) for product in
                        response_products]
    try:
        index = article_list.index(article)
        result[destination] = {
            'page': page,
            'position': index + 1
        }
        for task in tasks:
            task.cancel()
    except ValueError:
        pass


async def async_execute(
        query: str,
        article: int,
        destinations: list[int]
) -> dict:
    """Получение словаря с позицией товара в пункте выдачи заказа"""
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
