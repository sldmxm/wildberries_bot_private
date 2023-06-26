from csv import DictReader
from parser.models import Destination, Storehouse
from sys import exit

from django.core.management import BaseCommand


CSV_TABLES = {
    'Destinations': DictReader(open('../data/destination.csv')),
    'Storehouse': DictReader(open('../data/storehouse.csv')),
}


def delete_everything():
    Destination.objects.all().delete()
    Storehouse.objects.all().delete()


def print_attention():
    print(
        'Внимание! Будут уничтожены данные обо всех пунктов '
        'выдаи заказов и складах и заменены данными из CSV-файлов. '
        'Хотите продолжить ? [Y / N]: '
    )
    answer = input()
    if answer.upper() != 'Y':
        exit()


print_attention()
delete_everything()


class Command(BaseCommand):

    def handle(self, *args, **options):
        for value in CSV_TABLES['Destinations']:
            Destination.objects.get_or_create(
                pk=value['id'],
                city=value['city'],
                index=value['index'],
            )
        for value in CSV_TABLES['Storehouse']:
            Storehouse.objects.get_or_create(
                pk=value['id'],
                name=value['name'],
                index=value['index'],
            )
        print('Данные по умолчанию добавлены в базу данных')
