from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    """Регистрация модели в админке"""

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'phone_number',
    )

    search_fields = ('username',)
    list_filter = ('username',)
