from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import User

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    fieldsets = (("User", {"fields": ("name","age")}),) + tuple(
        auth_admin.UserAdmin.fieldsets
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
