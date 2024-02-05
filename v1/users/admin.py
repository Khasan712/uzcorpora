from django.contrib import admin
from v1.users.models import User, Manager, Admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'role', 'is_superuser', 'created_at', 'last_login')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'is_superuser', 'created_at', 'last_login')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'is_superuser', 'created_at', 'last_login')
