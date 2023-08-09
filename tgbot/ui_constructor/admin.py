from django.contrib import admin
from .models import ButtonConstructor


@admin.register(ButtonConstructor)
class ButtonConstructorAdmin(admin.ModelAdmin):
    """Регистрация модели ButtonConstructor в админке."""

    list_display = (
        'pk',
        'ui_control_id',
        'button_description',
        'default_text',
        'users_text',
    )

    search_fields = ('id', 'users_text',)
    list_filter = ('button_description',)
    readonly_fields = ['button_description', 'ui_control_id', 'default_text']
    ordering = ('pk',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
