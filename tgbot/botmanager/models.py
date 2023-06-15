from django.contrib.auth.models import AbstractUser
from django.db import models


MAX_LENGTH_USERNAME = 32
MAX_LENGTH_FIRST_NAME = 15
MAX_LENGTH_LAST_NAME = 20
MAX_LENGTH_PHONE_NUMBER = 12
USERNAME_VERBOSE = 'Имя пользователя в Telegram'
LAST_NAME_VERBOSE = 'Фамилия пользователя Telegram'
PHONE_NUMBER_VERBOSE = 'Номер телефона пользователя Telegram'


class TelegramUser(AbstractUser):
    """Базовая модель для управления данными пользователей ТГ бота"""

    username = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        unique=True,
        max_length=MAX_LENGTH_USERNAME,
    )
    first_name = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        max_length=MAX_LENGTH_FIRST_NAME,
    )
    last_name = models.CharField(
        verbose_name=LAST_NAME_VERBOSE,
        blank=True,
        null=True,
        max_length=MAX_LENGTH_LAST_NAME,
    )
    phone_number = models.CharField(
        verbose_name=PHONE_NUMBER_VERBOSE,
        blank=True,
        null=True,
        max_length=MAX_LENGTH_PHONE_NUMBER,
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return (
            f'{self.username}\n'
            f'{self.first_name}\n'
            f'{self.last_name}\n'
            f'{self.phone_number}.'
        )
