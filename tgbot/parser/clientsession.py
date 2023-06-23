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
        self.session = aiohttp.ClientSession(headers=self.headers, trust_env=True)
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
