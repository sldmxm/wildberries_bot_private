import aiohttp
from fake_useragent import UserAgent
from http import HTTPStatus


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

    #  todo: add get param
    async def get_data(self, link):
        try:
            async with self.session.get(link, timeout=10) as response:
                if response.status != HTTPStatus.OK:
                    return await self.get_data(link)
                return await response.content.read()
        except TimeoutError:
            print('tm')
            return await self.get_data(link)
        except Exception as untitled_exception:
            raise Exception
