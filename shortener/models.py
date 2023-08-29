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

