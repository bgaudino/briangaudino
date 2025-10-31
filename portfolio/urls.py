from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve

from portfolio import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("resume/", views.ResumeView.as_view(), name="resume"),
    path(
        "resume/download/", views.DownloadResumeView.as_view(), name="download_resume"
    ),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path(
        "contact/success/", views.ContactSuccessView.as_view(), name="contact_success"
    ),
    path("ai_chat/", views.CustomChatView.as_view(), name="chat"),
    path("ai_chat/", include("ai_chat.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
