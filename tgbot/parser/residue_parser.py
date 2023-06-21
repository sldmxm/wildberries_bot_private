from collections import defaultdict
from http import HTTPStatus

import aiohttp
from asgiref.sync import sync_to_async

from .constants import RESIDUE_PARSING_LINK
from .models import Storehouse


@sync_to_async
def get_storehouse_names():
    storehouses = Storehouse.objects.all()
    return {storehouse.index: storehouse.name for storehouse in storehouses}


async def get_residue(article):
    link = RESIDUE_PARSING_LINK.format(article=article)
    async with aiohttp.ClientSession() as session:
        response = await session.get(link)
        if response.status != HTTPStatus.OK:
            return False
        response_json = await response.json(content_type=response.content_type)
        try:
            response_data = response_json.get('data')
            response_product = response_data.get('products')[0]
            response_sizes = response_product.get('sizes')
        except AttributeError and IndexError:
            return False
        residual_sizes = defaultdict(int)
        residue_in_storehouses = defaultdict(int)
        storehouses_names = await get_storehouse_names()
        for size in response_sizes:
            try:
                size_name = size.get('name')
                stocks = size.get('stocks')
            except AttributeError:
                continue
            for stock in stocks:
                count = stock.get('qty', 0)
                try:
                    wh = stock.get('wh')
                    storehouse_name = storehouses_names.get(wh)
                    residue_in_storehouses[storehouse_name] += count
                except AttributeError:
                    pass
                residual_sizes[size_name] += count
        return residue_in_storehouses, residual_sizes
