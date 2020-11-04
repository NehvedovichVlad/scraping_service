
from django.urls import path

from scraping.views import home

urlpatterns = [
    path('', home),
]
