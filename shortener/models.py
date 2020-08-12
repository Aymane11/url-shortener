from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.forms.widgets import TextInput


def one_day_later():
    return timezone.now() + timezone.timedelta(days=1)


class ShortURL(models.Model):
    slug = models.SlugField(blank=True, null=True, unique=True)
    website = models.URLField(blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField(default=one_day_later)
    expired = models.BooleanField(default=False)

    def __str__(self):
        if self.expiration < timezone.now():
            self.expired = True
            return self.website + '(Expired)'
        else:
            return self.website
