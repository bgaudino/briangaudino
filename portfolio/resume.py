from django.forms.models import model_to_dict
from django.template.loader import render_to_string

from ai_chat.prompts.models import SystemPrompt
from weasyprint import HTML

from portfolio import models
from portfolio.decorators import cache_result


class ResumeBuilder:
    @cache_result("resume_chat_context")
    def generate_chat_context(self):
        system_prompt = SystemPrompt.objects.first()
        prompt = system_prompt.content if system_prompt else ""
        prompt += "\n\nYou can use this information to answer questions about Brian's professional background.\n\n"
        for model in [
            models.Job,
            models.Education,
            models.Technology,
            models.Project,
            models.Interest,
        ]:
            prompt += f"{model._meta.verbose_name_plural.title()}:\n"
            for instance in model.objects.published():
                prompt += f"{model_to_dict(instance)}:\n"
            prompt += "\n"
        return prompt

    def generate_pdf_context(self):
        personal_info = models.PersonalInfo.objects.first()
        contact = ([
            getattr(personal_info, field)
            for field in [
                "email",
                "phone",
            ]
            if getattr(personal_info, field)
        ] + personal_info.links) if personal_info else []
        context = {
            "personal_info": personal_info,
            "contact": contact,
            "jobs": models.Job.objects.published(),
            "education": models.Education.objects.published(),
            "skills": models.Technology.objects.published(),
            "interests": models.Interest.objects.published(),
        }
        return context

    @cache_result("resume_pdf")
    def generate_pdf(self, request):
        context = self.generate_pdf_context()
        html_content = render_to_string("documents/resume.html", context)
        pdf = HTML(
            string=html_content, base_url=request.build_absolute_uri()
        ).write_pdf()
        return pdf
