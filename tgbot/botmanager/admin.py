import requests
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse

from .models import Mailing, TelegramUser
from bot.core.settings import settings
from telegram import Bot

from asgiref.sync import async_to_sync


@async_to_sync
async def send_messages(bot, user_id, message):
    async with bot:
        await bot.send_message(user_id, message)


@async_to_sync
async def send_photo(bot, user_id, photo):
    async with bot:
        await bot.send_photo(user_id, photo)


@async_to_sync
async def send_document(bot, user_id, document):
    async with bot:
        await bot.send_document(user_id, document, write_timeout=10)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Регистрация модели в админке"""

    list_display = (
        'id',
        'username',
        'first_name',
        'telegram_id',
        'phone_number',
    )

    search_fields = ('id', 'username', 'phone_number',)
    list_filter = ('username',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Регистрация модели рассылок в админке"""
    change_form_template = 'admin/botmanager/mailing/change_form.html'

    list_display = (
        'id',
        'pub_date',
        'author',
        'content',
        'link',
        'image',
        'file_attache',
    )

    search_fields = ('id', 'author', 'content', 'recipients',)
    list_filter = ('author',)
    actions = ['add_all_users', ]

    @admin.action(description='Добавить всех пользователей в рассылку')
    def add_all_users(self, request, queryset):
        """Action для добавления всех подписчиков бота в адресаты сообщения."""
        users = TelegramUser.objects.all()
        for messge in queryset:
            for user in users:
                messge.recipients.add(user)

    def get_urls(self):
        """Добавляет пути для обработки кастомных кнопок:
        - Добавить всех пользователей
        - Отправить сообщение"""
        urls = super(MailingAdmin, self).get_urls()
        custom_urls = [
            path('<int:object_id>/change/add_all_users',
                 self.admin_site.admin_view(self.set_recipients),
                 name='recipients_view'),
            path('<int:object_id>/change/send_message',
                 self.admin_site.admin_view(self.send_message),
                 name='message_view'), ]
        return custom_urls + urls

    def set_recipients(self, request, object_id):
        """Вью-функция. Добавляет пользователей по нажатию кнопки."""
        self.add_all_users(
            request,
            queryset=Mailing.objects.filter(pk=object_id))
        return redirect(
            reverse('admin:botmanager_mailing_change',
                    kwargs={'object_id': object_id}))

    def send_message(self, request, object_id):
        """Отправляет соощение в телеграмм"""
        bot = Bot(token=settings.telegram_token)
        message = Mailing.objects.get(pk=object_id)
        for recipient in message.recipients.all():
            send_messages(bot, recipient.telegram_id, message.content)
            if message.image:
                send_photo(bot, recipient.telegram_id, message.image)
            if message.file_attache:
                send_document(bot, recipient.telegram_id, message.file_attache)
        return redirect(reverse('admin:botmanager_mailing_change',
                        kwargs={'object_id': object_id}))
