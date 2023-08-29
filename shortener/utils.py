import random
import string

from django.utils import timezone

from .models import ShortURL


def random_str() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=5))


def is_slug_available(slug: str) -> bool:
    # Avaliable if no other active short url has the same slug
    return not ShortURL.objects.filter(slug=slug, active=True).exists()


def create_available_random_slug() -> str:
    slug = random_str()
    while not is_slug_available(slug):
        slug = random_str()
    return slug


def is_active(short: ShortURL) -> bool:
    return short.active and timezone.now() < short.expiration


def expire(short: ShortURL) -> None:
    short.active = False
    short.save()
