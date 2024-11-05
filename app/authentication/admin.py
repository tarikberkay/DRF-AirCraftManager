from django.contrib import admin
from authentication.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
    ]

    search_fields = [
        "email",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
