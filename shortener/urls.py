from django.conf.urls import url
from .views import *

app_name = 'shortener'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^thanks/(?P<slug>[a-zA-Z0-9]+)$', thanks, name='thanks'),
    url(r'^(?P<slug>[a-zA-Z0-9]+)$', redirect_to_website, name='redirect_to_website'),
]
