from django.contrib import admin

from user_master.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "mobile_no")
    list_filter = ("created_at",)
    search_fields = ("first_name__icontains", "last_name__icontains", "email__icontains")

