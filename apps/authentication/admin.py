from django.contrib import admin
from authentication.models import Account, Rate

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "balance", "is_superuser")
    readonly_fields = ("username", "balance", "password", "groups", "user_permissions",
                        "is_staff", "is_superuser", "is_active", "last_login", "token")

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("customer", "vendor", "vote")
    readonly_fields = ("customer", "vendor", "vote")