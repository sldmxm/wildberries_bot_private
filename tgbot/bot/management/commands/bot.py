from django.core.management.base import BaseCommand

from bot.conversations.main_application import main


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        main()
