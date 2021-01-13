from django.contrib import admin

from common.models import LookUp, LookUpMapping


@admin.register(LookUp)
class LookUpAdmin(admin.ModelAdmin):
    list_display = ("lu_code", "lu_desc")
    list_filter = ("lu_cr_at",)
    search_fields = ("lu_code__icontains", "lu_desc__icontains")


@admin.register(LookUpMapping)
class LookUpMappingAdmin(admin.ModelAdmin):
    list_display = ("lum_code", "lum_desc", "lum_head")
    list_filter = ("lum_cr_at",)
    search_fields = ("lum_code__icontains", "lum_desc__icontains")

