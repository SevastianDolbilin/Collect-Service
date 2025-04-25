from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from core.models import User

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """Настройка отображения пользователей в админке."""

    list_display = (
        "id", "username", "email", "first_name", "last_name", "is_active"
    )
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff")
