from django.db import models

MAX_LENGTH_USERNAME = 32
MAX_LENGTH_FIRST_NAME = 15
MAX_LENGTH_ID = 10
MAX_LENGTH_PHONE_NUMBER = 12
NAME_VERBOSE = 'Имя пользователя'
USERNAME_VERBOSE = 'Имя пользователя в Telegram'
ID_VERBOSE = 'Идентификатор пользователя Telegram'
CREATED_AT_VERBOSE = 'Дата первого запроса'


class TelegramUser(models.Model):
    """Базовая модель для управления данными пользователей ТГ бота"""

    username = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=NAME_VERBOSE,
        max_length=MAX_LENGTH_FIRST_NAME,
    )
    telegram_id = models.CharField(
        verbose_name=ID_VERBOSE,
        max_length=MAX_LENGTH_ID,
    )

    created_at = models.DateTimeField(
        verbose_name=CREATED_AT_VERBOSE,
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return (
            f'Пользователь: {self.username} ID: {self.telegram_id}'
        )
