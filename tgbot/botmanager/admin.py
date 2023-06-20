from django.contrib import admin

from .models import TelegramUser


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
