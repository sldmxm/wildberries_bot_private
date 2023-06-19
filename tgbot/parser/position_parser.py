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


loop = asyncio.get_event_loop()


async def get_total_positions(query: str, destination: int) -> int:
    """получение общего количества товаров по запросу"""
    link = TOTAL_PRODUCTS_LINK.format(query=query, destination=destination)
    async with aiohttp.ClientSession() as session:
        response = await session.get(link)
        response_json = await response.json(content_type=response.content_type)
        response_data = response_json.get('data', {})
        return response_data.get('total', 0)


async def parse_page(
        session: aiohttp.ClientSession,
        page: int,
        query: str,
        article: int,
        destination: int,
        tasks: list,
        result: dict
) -> None:
    """парсинг страниц с товаром"""
    link = PAGE_PARSING_LINK.format(
        destination=destination,
        page=str(page),
        query=query
    )
    response = await session.get(link)
    if response.status != HTTPStatus.OK:
        return
    response_json = await response.json(content_type=response.content_type)
    response_data = response_json.get('data', {})
    response_products = response_data.get('products', [])
    article_list = [product.get('id', None) for product in response_products]
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
    result = {destination: {} for destination in destinations}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for destination in destinations:
            total_positions = await get_total_positions(query, destination)
            page_tasks = []
            for page in range(1, min(ceil(total_positions / 100), 61)):
                task = asyncio.ensure_future(parse_page(
                    session,
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
    result_text = ''
    async for destination in Destination.objects.all():
        result = results.get(destination.index, {})
        page = result.get('page', None)
        position = result.get('position', None)
        prev_page = result.get('prev_page', None)
        prev_position = result.get('prev_position', None)
        if page is None or position is None:
            result_text += PRODUCT_POSITION_NOT_FOUND_MESSAGE.format(
                city=destination.city
            )
        elif prev_page is not None and prev_position is not None:
            if page > prev_page:
                page_arrow = '↑'
            elif page == prev_page:
                page_arrow = '●'
            else:
                page_arrow = '↓'
            if position > prev_position:
                position_arrow = '↑'
            elif position == prev_position:
                position_arrow = '●'
            else:
                position_arrow = '↓'
            result_text += PRODUCT_POSITION_SCHEDULE_MESSAGE.format(
                city=destination.city,
                page=page,
                position=position,
                prev_page=prev_page,
                prev_position=prev_position,
                position_difference=abs(prev_position - position),
                page_difference=abs(prev_page - page),
                page_arrow=page_arrow,
                position_arrow=position_arrow
            )
        else:
            result_text += PRODUCT_POSITION_MESSAGE.format(
                city=destination.city,
                page=page,
                position=position
            )
    return result_text


async def get_position(product_id: int, query: str) -> dict:
    query = '%20'.join(query.split(' '))
    destinations = []
    async for destination in Destination.objects.all():
        destinations.append(destination.index)
    return await async_execute(
        query,
        product_id,
        destinations
    )
