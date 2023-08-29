from django.conf import settings
from django.db import models
from django.utils import timezone


def expiration_time():
    return timezone.now() + settings.SHORTENER_EXPIRATION_DURATION


class ShortURL(models.Model):
    slug = models.SlugField(blank=False, null=False, unique=False)
    website = models.URLField(blank=False, null=False)
    creation_date = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField(default=expiration_time)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.slug} -> {self.website}, active: {self.active}"

    class Meta:
        get_latest_by = "creation_date"
        ordering = ["-creation_date"]
        verbose_name = "Short URL"
        verbose_name_plural = "Short URLs"
