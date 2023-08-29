from django.db import models
from django.utils import timezone
from django.conf import settings

def expiration_time():
    return timezone.now() + settings.SHORTENER_EXPIRATION_DURATION


class ShortURL(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True)
    website = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField(default=expiration_time)
    expired = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ["-creation_date"]
        verbose_name = "Short URL"
        verbose_name_plural = "Short URLs"