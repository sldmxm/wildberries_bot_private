from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Регистрация модели в админке."""
    list_display = (
        'pk', 'role', 'username', 'email',
        'first_name', 'last_name',
    )
    search_fields = ('username', 'email',)
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
