from django.contrib import admin

from .models import ShortURL

# Register your models here.


class ShortAdmin(admin.ModelAdmin):
    list_display = ["slug", "website", "expired", "creation_date", "expiration"]
    actions = ["expire", "unexpire"]

    def expire(self, request, queryset):
        for link in queryset:
            link.expired = True
            link.save()

    expire.short_description = "Expire selected"

    def unexpire(self, request, queryset):
        for link in queryset:
            link.expired = False
            link.save()

    unexpire.short_description = "Unexpire selected"

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False


admin.site.register(ShortURL, ShortAdmin)
