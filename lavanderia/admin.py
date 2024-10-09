from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lavanderia.models import LavanderiaUser

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(LavanderiaUser, UserAdmin)