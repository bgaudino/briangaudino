from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator

from portfolio.forms import ContactForm
from portfolio.models import Education, Job, Project


@method_decorator(cache_page(None), name="dispatch")
class IndexView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.all()
        context["jobs"] = Job.objects.all()
        context["educations"] = Education.objects.all()
        return context


class ContactView(CreateView):
    template_name = "portfolio/contact.html"
    form_class = ContactForm
    success_url = "/"
