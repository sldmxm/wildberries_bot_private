from django.test import TestCase

from ..models import Destination


class ParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TEST_ARTICLE = 36704403
        cls.TEST_QUERY = 'футболка женская'
        Destination.objects.bulk_create([
            Destination(city='Москва', index='-240229'),
            Destination(city='Санкт - Петербург', index='-1121517'),
            Destination(city='Краснодар', index='12358058'),
            Destination(city='Казань', index='-2133462'),
            Destination(city='Екатеринбург', index='-5803327'),
            Destination(city='Владивосток', index='123586013'),
        ])
