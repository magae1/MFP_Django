from django.contrib import admin

from .models import Account, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'last_login']
    list_filter = ['last_login', 'date_joined', 'is_active', 'is_staff']
    search_fields = ['username', 'email']

    inlines = [ProfileInline]


