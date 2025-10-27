from pathlib import Path

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator

from portfolio.forms import ContactForm
from portfolio.models import Content, Education, Job, Project, Technology


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


class IndexView(HTMXMixin, CacheForeverMixin, TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["content"] = Content.objects.published().get(title="about").content
        except Content.DoesNotExist:
            context["content"] = None
        return context


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
    success_url = "/"
