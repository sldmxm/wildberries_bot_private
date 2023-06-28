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
        'created_at',
    )

    search_fields = ('id', 'username')
    list_filter = ('username',)


admin.site.site_title = 'Административная панель бота'
admin.site.site_header = 'Административная панель бота'
