from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

MAX_LENGTH_USERNAME = 32
MAX_LENGTH_FIRST_NAME = 15
MAX_LENGTH_ID = 10
MAX_LENGTH_PHONE_NUMBER = 12
MAX_LENGTH_BUTTON_TEXT = 256
NAME_VERBOSE = 'Имя пользователя'
USERNAME_VERBOSE = 'Имя пользователя в Telegram'
USERNAME_FOR_NULL_TG_USERNAME = 'tg-пользователь не указал username'
ID_VERBOSE = 'Идентификатор пользователя Telegram'
CREATED_AT_VERBOSE = 'Дата первого запроса'
BUTTON_VERBOSE = 'Описание функционала кнопки'
UI_CONTROL_ID = 'ID редактируемого элемента'
DEFAULT_TEXT = 'Текст по умолчанию'
USERS_TEXT = 'Текст пользователя'



class TelegramUser(models.Model):
    """Базовая модель для управления данными пользователей ТГ бота"""

    username = models.CharField(
        verbose_name=USERNAME_VERBOSE,
        max_length=MAX_LENGTH_USERNAME,
    )
    first_name = models.CharField(
        verbose_name=NAME_VERBOSE,
        max_length=MAX_LENGTH_FIRST_NAME,
    )
    telegram_id = models.CharField(
        verbose_name=ID_VERBOSE,
        max_length=MAX_LENGTH_ID,
        unique=True,
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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = USERNAME_FOR_NULL_TG_USERNAME
        super().save(*args, **kwargs)


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
        upload_to='static/images/',
        blank=True,)

    file_attache = models.FileField(
        verbose_name='Прикрепленный файл',
        upload_to='static/files/',
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
        verbose_name = 'Рассылку'
        verbose_name_plural = 'Рассылки Telegram'

    def __str__(self):
        return f'{self.pub_date}: ({self.author}) - {self.content[:15]}'


class ButtonConstructor(models.Model):
    """Модель конструктора кнопок."""

    ui_control_id = models.CharField(
        verbose_name=UI_CONTROL_ID,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    button_description = models.CharField(
        verbose_name=BUTTON_VERBOSE,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    default_text = models.CharField(
        verbose_name=DEFAULT_TEXT,
        max_length=MAX_LENGTH_BUTTON_TEXT,
    )
    users_text = models.CharField(
        verbose_name=USERS_TEXT,
        max_length=MAX_LENGTH_BUTTON_TEXT,
        blank=True,
    )

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return self.ui_control_id
