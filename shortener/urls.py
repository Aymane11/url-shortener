from django.urls import re_path

from .views import home, redirect_to_website, thanks

app_name = "shortener"

urlpatterns = [
    re_path(r"^$", home, name="home"),
    re_path(r"^thanks/(?P<slug>[a-zA-Z0-9]+)$", thanks, name="thanks"),
    re_path(
        r"^(?P<slug>[a-zA-Z0-9]+)$", redirect_to_website, name="redirect_to_website"
    ),
]
