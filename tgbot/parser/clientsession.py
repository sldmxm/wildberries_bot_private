import aiohttp
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
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    #  todo: add get param
    async def get(self, link):
        try:
            async with self.session.get(link, timeout=10) as response:
                if response.status != HTTPStatus.OK:
                    return await self.get(link)
                return await response.content.read()
        except TimeoutError:
            return await self.get(link)
