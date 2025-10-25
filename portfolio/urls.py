from django.contrib import admin
from django.urls import path

from portfolio.views import ContactView, IndexView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("admin/", admin.site.urls),
]
