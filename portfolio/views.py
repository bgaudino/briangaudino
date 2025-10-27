from pathlib import Path

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator

from portfolio.forms import ContactForm
from portfolio.models import Content, Education, Interest, Job, Project, Technology

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


CHAT_CACHE_KEY = "custom_ai_chat_system_prompt"


class CustomChatView(AIChatView):
    def get_system_prompt(self):
        from django.forms.models import model_to_dict

        prompt = cache.get(CHAT_CACHE_KEY)
        if prompt:
            return prompt
        prompt = super().get_system_prompt() or ""
        prompt += "\n\nHere is some information about Brian:\n"
        for model in (Job, Education, Technology, Project, Interest):
            prompt += f"\n\n{model._meta.verbose_name_plural.title()}:\n"
            items = model.objects.published()
            for item in items:
                prompt += str(model_to_dict(item)) + "\n"
        cache.set(CHAT_CACHE_KEY, prompt)
        return prompt
