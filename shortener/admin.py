from django.contrib import admin

from .models import ShortURL
from .utils import expire

# Register your models here.


@admin.register(ShortURL)
class ShortAdmin(admin.ModelAdmin):
    list_display = ["slug", "website", "active", "creation_date", "expiration"]
    actions = ["expire"]
    search_fields = ["slug", "website"]

    def expire(self, request, queryset):
        for link in queryset:
            expire(link)

    expire.short_description = "Expire selected"

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
