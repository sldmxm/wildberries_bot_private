from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'role', 'username')
    search_fields = ('role',)


admin.site.register(User, UserAdmin)
