from django.test import TestCase
import logging
import re

from bot.constants.text import LOG_MESSAGE_ERROR_GET_DATA_PATTERN
from bot.core.logging import logger
from ..models import Destination


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


class ParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TEST_ARTICLE = 36704403
        cls.TEST_QUERY = 'футболка женская'
        cls.LOG_ERROR_PATTERN = LOG_MESSAGE_ERROR_GET_DATA_PATTERN
        Destination.objects.bulk_create([
            Destination(city='Москва', index='-240229'),
            Destination(city='Санкт - Петербург', index='-1121517'),
            Destination(city='Краснодар', index='12358058'),
            Destination(city='Казань', index='-2133462'),
            Destination(city='Екатеринбург', index='-5803327'),
            Destination(city='Владивосток', index='123586013'),
        ])

    def setUp(self):
        self.logger = logger
        self.mock_error_calls = []

    def record_mock_error_call(self, *args):
        match = re.search(self.LOG_ERROR_PATTERN, args[0])
        if match:
            self.mock_error_calls.append(match.group(1))

    def tearDown(self):
        self.mock_error_calls = []

