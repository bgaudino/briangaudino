from pathlib import Path

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, TemplateView

from portfolio.forms import ContactForm
from portfolio.models import Content, Education, Job, Project, Technology
from portfolio.resume import ResumeBuilder

from ai_chat.views import ChatView as AIChatView


class HTMXMixin:
    def get_template_names(self):
        if self.request.is_htmx:
            path = Path(self.template_name)
            return str(path.parent / "partials" / f"_{path.name}")

        return super().get_template_names()


class CacheForeverMixin:
    @method_decorator(vary_on_headers("HX-Request"))
    @method_decorator(cache_page(None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ContentView(HTMXMixin, CacheForeverMixin, TemplateView):
    template_name = "portfolio/content.html"
    content_name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.content_name:
            raise ValueError("content_name must be set for ContentView")

    def get_context_data(self, **kwargs):
        content = Content.objects.published().filter(title=self.content_name).first()
        kwargs["content"] = kwargs[self.content_name] = content
        return super().get_context_data(**kwargs)


class IndexView(ContentView):
    template_name = "portfolio/index.html"
    content_name = "tagline"


class AboutView(ContentView):
    content_name = "about"


class ProjectsView(HTMXMixin, CacheForeverMixin, TemplateView):
    template_name = "portfolio/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.published()
        return context


class ResumeView(HTMXMixin, CacheForeverMixin, TemplateView):
    template_name = "portfolio/resume.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jobs"] = Job.objects.published()
        context["educations"] = Education.objects.published()
        context["skills"] = Technology.objects.published()
        return context


class ContactView(HTMXMixin, CreateView):
    template_name = "portfolio/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("index")


class CustomChatView(AIChatView):
    def get_system_prompt(self):
        resume = ResumeBuilder()
        return resume.generate_chat_context()


class DownloadResumeView(TemplateView):
    def get(self, request, *args, **kwargs):
        from .resume import ResumeBuilder

        resume = ResumeBuilder()
        pdf_file = resume.generate_pdf(request)
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'filename="Brian Gaudino.pdf"'
        return response
