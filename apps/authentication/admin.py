from django.contrib import admin
from authentication.models import Account, VendorRate

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("username", "balance", "is_superuser")
    readonly_fields = ("username", "balance", "password", "groups", "user_permissions",
                        "is_staff", "is_superuser", "is_active", "last_login", "token")

@admin.register(VendorRate)
class VendorRateAdmin(admin.ModelAdmin):
    list_display = ("customer", "vendor", "vote")
    readonly_fields = ("customer", "vendor", "vote")