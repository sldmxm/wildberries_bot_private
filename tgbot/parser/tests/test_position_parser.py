import time

from tqdm import tqdm
from unittest.mock import patch
from collections import Counter

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
        После каждой порции запросов выводит ошибки ответа сервера
        """
        with (
            patch.object(self.logger, "error", side_effect=self.record_mock_error_call),
            patch.object(self.logger, "info"),
        ):
            for index, request_count in enumerate(self.SERIES_REQUESTS):
                for _ in tqdm(range(request_count)):
                    await position_parser.get_position(
                        self.TEST_ARTICLE, self.TEST_QUERY
                    )
            if self.mock_error_calls:
                print("Сводный отчет об ошибках:")
                for error_call,  count in Counter(self.mock_error_calls).items():
                    print(f'{error_call}: {count}')

                if index < len(self.SERIES_REQUESTS) - 1:
                    time.sleep(self.SERIES_REQUESTS_PAUSE)
