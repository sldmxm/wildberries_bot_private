from django.contrib import admin

from .models import UserAction


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    """Регистрация модели в админке"""

    list_display = (
        'id',
        'telegram_user',
        'datetime',
        'action',
    )

    search_fields = ('id', 'telegram_user')
    list_filter = ('action',)
