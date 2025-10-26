from django.contrib import admin
from django.urls import path, include

from portfolio.views import ContactView, IndexView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("ai_chat/", include("ai_chat.urls")),
    path("admin/", admin.site.urls),
]
