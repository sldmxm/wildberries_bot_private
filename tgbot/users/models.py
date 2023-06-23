from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Базовая модель для управления данными пользователей админки"""
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )

    username = models.CharField(
        verbose_name='Логин',
        help_text='Укажите логин для входа в аккаунт',
        max_length=50,
        unique=True,
        null=False,
        blank=False)

    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Укажите ваше имя',
        max_length=50,
        null=False,
        blank=False)

    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Укажите вашу фамилию',
        max_length=100,
        null=False,
        blank=False)

    role = models.CharField(
        verbose_name='Роль пользователя в системе',
        help_text='Укажите права доступа пользователя',
        max_length=30,
        choices=USER_ROLES,
        default=USER)

    email = models.EmailField(
        verbose_name='Email пользователя',
        help_text='Укажите вашу почту',
        max_length=254,
        unique=True,
        null=False,
        blank=False)

    phone_number = PhoneNumberField(
        verbose_name='Номер телефона пользователя',
        help_text='Укажите ваш номер телефона',
        null=True,
        blank=True)

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['id']

    def __str__(self):
        return self.username
