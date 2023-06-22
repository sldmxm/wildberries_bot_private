from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

MAX_LENGTH_USERNAME = 32
MAX_LENGTH_FIRST_NAME = 15
MAX_LENGTH_ID = 10
MAX_LENGTH_PHONE_NUMBER = 12
USERNAME_VERBOSE = 'Имя пользователя в Telegram'
ID_VERBOSE = 'Идентификатор пользователя Telegram'
PHONE_NUMBER_VERBOSE = 'Номер телефона пользователя Telegram'


class TelegramUser(models.Model):
    """Базовая модель для управления данными пользователей ТГ бота"""

    username = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        max_length=MAX_LENGTH_FIRST_NAME,
    )
    telegram_id = models.CharField(
        verbose_name=ID_VERBOSE,
        max_length=MAX_LENGTH_ID,
    )
    phone_number = models.CharField(
        verbose_name=PHONE_NUMBER_VERBOSE,
        max_length=MAX_LENGTH_PHONE_NUMBER,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'

    def __str__(self):
        return (
            f'Пользователь: {self.username} ID: {self.telegram_id}'
        )


class Mailing(models.Model):
    """Модель сообщения рассылки пользователям ТГ бота."""

    author = models.ForeignKey(
        User,
        related_name='mailings',
        on_delete=models.CASCADE,
        verbose_name='Автор',)

    content = models.TextField(
        verbose_name='Содержание сообщения',)

    link = models.URLField(
        verbose_name='Прикрепленная ссылка',
        blank=True,)

    image = models.ImageField(
        verbose_name='Прикрепленное изображение',
        upload_to='tgbot/botmanager/images/',
        blank=True,)

    file_attache = models.FileField(
        verbose_name='Прикрепленный файл',
        upload_to='tgbot/botmanager/files/',
        blank=True,)

    recipients = models.ManyToManyField(
        TelegramUser,
        related_name='mailings',
        verbose_name='Получатели',
        blank=True,)

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылки'

    def __str__(self):
        return f'{self.pub_date}: ({self.author}) - {self.content[:15]}'
