from .fixtures import ParserTests
from parser import position_parser


class PostViewsTests(ParserTests):
    MAX_REQUESTS = 100

    async def test_get_position_max_requests_limit(self):
        """
        Проверяет, будет ли заблокирован парсер
        при MAX_REQUESTS запросов.
        """
        blocked = False
        try:
            for i in range(self.MAX_REQUESTS):
                await position_parser.get_position(
                    self.TEST_ARTICLE, self.TEST_QUERY
                )
        except Exception as e:
            if "403" in str(e):
                blocked = True
        self.assertFalse(
            blocked,
            f'Сайт заблокировал доступ в результате '
            f'{self.MAX_REQUESTS} запросов.'
        )
