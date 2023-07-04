from http import HTTPStatus

import aiohttp
from aiohttp.client_exceptions import ClientError
from fake_useragent import UserAgent


class ClientSession:
    def __init__(self):
        ua = UserAgent()
        self. headers = {
            'User-Agent': ua.random
        }
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            trust_env=True
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_data(self, link):
        """Асинхронное получение данных по ссылки"""
        try:
            async with self.session.get(link, timeout=10) as response:
                if response.status == HTTPStatus.OK:
                    return await response.content.read()
        except TimeoutError:
            pass
        except ClientError:
            pass
        return await self.get_data(link)
