from django.contrib import admin

from .models import Account, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "identifier", "last_login"]
    fields = [("identifier", "id"), "last_login", 'is_staff', 'is_active']
    list_display = ['identifier', 'email', 'last_login']
    list_filter = ['last_login', 'date_joined', 'is_active', 'is_staff']
    search_fields = ['username', 'email']

    inlines = [ProfileInline]
