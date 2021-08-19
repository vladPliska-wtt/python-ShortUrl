from django.urls import path
from .views import UrlView


urlpatterns = [
    path('', UrlView.makeUrl),
    path('<str:link>', UrlView.getUrl)
]
