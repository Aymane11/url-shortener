from django.contrib import admin
from .models import *

# Register your models here.

class ShortAdmin(admin.ModelAdmin):
    list_display = ['website', 'slug', 'expired', 'creation_date', 'expiration']
    actions = ['expire','unexpire']

    def expire(self, request, queryset):
        for link in queryset:
            link.expired = True
        link.save()
    expire.short_description = 'Expire all links'

    def unexpire(self, request, queryset):
        for link in queryset:
            link.expired = False
        link.save()
    unexpire.short_description = 'Unexpire all links'

admin.site.register(ShortURL, ShortAdmin)