from http import HTTPStatus

import aiohttp
from aiohttp.client_exceptions import ClientError
from fake_useragent import UserAgent

from bot.constants import text
from bot.core.logging import logger


class ClientSession:
    def __init__(self, headers=None):
        ua = UserAgent()
        self.headers = {
            'User-Agent': ua.random
        }
        if headers:
            self.headers.update(headers)
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
        """Асинхронное получение данных по ссылке."""
        try:
            async with self.session.get(link, timeout=10) as response:
                if response.status == HTTPStatus.OK:
                    return await response.content.read()
                else:
                    response.raise_for_status()
        except TimeoutError:
            pass
        except ClientError as e:
            logger.error(text.LOG_MESSAGE_ERROR_GET_DATA.format(error=e))
        return await self.get_data(link)
