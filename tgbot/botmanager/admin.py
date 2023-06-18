from django.contrib import admin

from .models import TelegramUser, Mailing


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

    list_display = (
        'id',
        'pub_date',
        'author',
        'content_type',
        'content',
    )

    search_fields = ('id', 'author', 'content', 'recipients',)
    list_filter = ('author', 'content_type',)
