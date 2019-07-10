from django.contrib import admin
from django.contrib.auth.admin import Group, UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

# Register your models here.

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'nickname', 'is_staff', 'is_active', 'is_superuser')
