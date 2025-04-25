from django.contrib import admin

from .models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Админ модель Сборов."""
    list_display = ("title", "author", "goal_amount", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Админ модель Платежей."""
    list_display = ("collect", "donor", "amount", "created_at")
    search_fields = ("collect__title", "donor__username")
    list_filter = ("created_at",)
