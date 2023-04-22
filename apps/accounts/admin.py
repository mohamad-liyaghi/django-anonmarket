from django.contrib import admin
from accounts.models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "balance", "is_superuser")
    readonly_fields = ("username", "balance", "password", "groups", "user_permissions",
                        "is_staff", "is_superuser", "is_active", "last_login", "token")

