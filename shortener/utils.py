import random
import string

from django.utils import timezone

from .models import ShortURL


def random_str() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=5))


def is_slug_available(slug: str) -> bool:
    return not ShortURL.objects.filter(slug=slug).exists()


def create_random_slug() -> str:
    slug = random_str()
    while not is_slug_available(slug):
        slug = random_str()
    return slug


def is_expired(short: ShortURL) -> bool:
    return short.expired or short.expiration < timezone.now()
