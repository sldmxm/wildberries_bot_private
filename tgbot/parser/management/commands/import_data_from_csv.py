from csv import DictReader
from botmanager.models import ButtonConstructor
from parser.models import Destination, Storehouse
from sys import exit

from django.core.management import BaseCommand


CSV_TABLES = {
    'Destinations': DictReader(
        open('../data/destination.csv', encoding='utf-8')
    ),
    'Storehouse': DictReader(
        open('../data/storehouse.csv', encoding='utf-8')
    ),
    'ButtonConstructor': DictReader(
        open('../data/buttons.csv', encoding='utf-8')
    ),
}


def delete_everything():
    Destination.objects.all().delete()
    Storehouse.objects.all().delete()
    ButtonConstructor.objects.all().delete()


def print_attention():
    print(
        'Внимание! Будут уничтожены данные обо всех пунктах '
        'выдачи заказов и складах и заменены данными из CSV-файлов. '
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
        for value in CSV_TABLES['ButtonConstructor']:
            ButtonConstructor.objects.get_or_create(
                pk=value['id'],
                button_name=value['button_name'],
                button_description=value['button_description'],
                default_text=value['default_text'],
            )
        print('Данные по умолчанию добавлены в базу данных')
