import time
from tqdm import tqdm

from .fixtures import ParserTests
from parser import position_parser


class PostViewsTests(ParserTests):
    SERIES_REQUESTS = (250, 500, 1000,)
    SERIES_REQUESTS_PAUSE = 3600

    async def test_get_position_requests_limit(self,):
        """
        Проверяет, будет ли заблокирован парсер
        при серии запросов SERIES_REQUESTS
        с паузой между ними SERIES_REQUESTS_PAUSE.
        """
        for index, request_count in enumerate(self.SERIES_REQUESTS):
            blocked = False
            try:
                for _ in tqdm(range(request_count)):
                    await position_parser.get_position(
                        self.TEST_ARTICLE, self.TEST_QUERY
                    )
            except Exception as e:
                if "403" in str(e):
                    blocked = True
            self.assertFalse(
                blocked,
                f'Сайт заблокировал доступ в результате '
                f'{request_count} запросов.'
            )
            if index < len(self.SERIES_REQUESTS) - 1:
                time.sleep(self.SERIES_REQUESTS_PAUSE)
