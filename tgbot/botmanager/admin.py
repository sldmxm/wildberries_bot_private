from asgiref.sync import async_to_sync
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from telegram import Bot

from .models import Mailing, TelegramUser
from bot.core.settings import settings


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Регистрация модели TelegramUser в админке"""

    list_display = (
        'id',
        'username',
        'first_name',
        'telegram_id',
        'created_at',
    )

    search_fields = ('id', 'username')
    list_filter = ('username',)


admin.site.site_title = 'Административная панель бота'
admin.site.site_header = 'Административная панель бота'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Регистрация модели Mailing в админке"""
    # change_form_template = 'admin/botmanager/mailing/change_form.html'

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

    def response_change(self, request, obj):
        if '_add_all_users' in request.POST:
            self.set_recipients(request, obj.id)
            return redirect(reverse('admin:botmanager_mailing_change',
                                    kwargs={'object_id': obj.id}))
        elif '_send_mailing' in request.POST:
            self.send_message(request, obj.id)
            return redirect(reverse('admin:botmanager_mailing_change',
                                    kwargs={'object_id': obj.id}))

        else:
            return super().response_change(request, obj)

    @async_to_sync
    async def send_messages(self, bot, user_id, message):
        """Конвертер для асинхронной отправки текстового сообщения"""
        async with bot:
            await bot.send_message(user_id, message)

    @async_to_sync
    async def send_photo(self, bot, user_id, photo):
        """Конвертер для асинхронной отправки фото"""
        async with bot:
            await bot.send_photo(user_id, photo)

    @async_to_sync
    async def send_document(self, bot, user_id, document):
        """Конвертер для асинхронной отправки файла"""
        async with bot:
            await bot.send_document(user_id, document, write_timeout=10)

    @admin.action(description='Добавить всех пользователей в рассылку')
    def add_all_users(self, request, queryset):
        """Action для добавления всех подписчиков бота в адресаты сообщения."""
        users = TelegramUser.objects.all()
        for messge in queryset:
            for user in users:
                messge.recipients.add(user)

    def set_recipients(self, request, object_id):
        """Добавляет пользователей по нажатию кнопки."""
        self.add_all_users(
            request,
            queryset=Mailing.objects.filter(pk=object_id))

    def send_message(self, request, object_id):
        """Отправляет соощение в телеграмм."""
        bot = Bot(token=settings.telegram_token)
        message = Mailing.objects.get(pk=object_id)

        for recipient in message.recipients.all():
            if message.image:
                self.send_photo(bot, recipient.telegram_id, message.image)
            message_text = '\n'.join(
                [message.content, message.link]
                ) if message.link else message.content
            self.send_messages(bot, recipient.telegram_id, message_text)
            if message.file_attache:
                self.send_document(bot, recipient.telegram_id,
                                   open(str(message.file_attache), 'rb'))
