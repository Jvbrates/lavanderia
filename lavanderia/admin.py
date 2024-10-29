from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lavanderia.models import LavanderiaUser, Washer


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'bolsista',
                ),
            },
        ),
    )


admin.site.register(LavanderiaUser, CustomUserAdmin)
admin.site.register(Washer)
