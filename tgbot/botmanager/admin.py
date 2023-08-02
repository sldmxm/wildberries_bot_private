from time import sleep

import celery
from django.contrib import admin, messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse

from .models import Mailing, TelegramUser
from .tasks import schedule_send_message


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Регистрация модели TelegramUser в админке."""

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
admin.site.unregister(Group)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Регистрация модели Mailing в админке."""

    list_display = (
        'id',
        'pub_date',
        'author',
        'content',
        'link',
        'image',
        'file_attache',)
    list_display_links = ('id', 'pub_date',)

    search_fields = ('id', 'author__username', 'content',)
    list_filter = ('author__username',)
    actions = ['action_add_all_users',
               'action_send_message', ]

    def response_change(self, request, obj):
        """Обработка нажатий кастомных кнопок."""
        if '_add_all_users' in request.POST:
            self.set_recipients(request, obj.id)
            return redirect(reverse(
                'admin:botmanager_mailing_change',
                kwargs={'object_id': obj.id})
            )
        if '_send_mailing' in request.POST:
            self.schedule_send(obj.id, request)
            return redirect(reverse(
                'admin:botmanager_mailing_change',
                kwargs={'object_id': obj.id})
            )
        return super().response_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Значение поля author по умолчанию."""
        form = super(MailingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

    @admin.action(description='Добавить всех пользователей в рассылку')
    def action_add_all_users(self, request, queryset):
        """Action для добавления всех подписчиков бота в адресаты сообщения."""
        users = TelegramUser.objects.all()
        for messge in queryset:
            for user in users:
                messge.recipients.add(user)

    @admin.action(description='Отправить рассылку в Telegram')
    def action_send_message(self, request, queryset):
        """Action для рассылки в Telegram."""
        for messge in queryset:
            self.schedule_send(messge.id, request)
            return
        messages.add_message(
            request,
            messages.WARNING,
            'Нет данных для рассылки'
        )

    def set_recipients(self, request, object_id):
        """Добавляет пользователей по нажатию кнопки."""
        self.action_add_all_users(
            request,
            queryset=Mailing.objects.filter(pk=object_id))

    def schedule_send(self, object_id, request):
        task = schedule_send_message.delay(object_id=object_id)
        sleep(2)
        result = celery.result.AsyncResult(task.id)
        if not result.result:
            messages.add_message(
                request,
                messages.ERROR,
                'Ошибка в содержании сообщения'
            )
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                'Рассылка в Telegram началась'
            )
