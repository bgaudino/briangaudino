import os

from django import forms
from django.conf import settings

import requests

from portfolio.models import Contact, Technology


def google_captcha_validator(value):
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": value,
        },
    )

    if not response.json().get("success"):
        raise forms.ValidationError("Invalid reCAPTCHA")


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["g-recaptcha-response"] = forms.fields.CharField(
            widget=forms.HiddenInput,
            validators=[google_captcha_validator],
            required=True,
        )


class ProjectFilterForm(forms.Form):
    technology = forms.ModelChoiceField(
        queryset=Technology.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "hx-get": "/projects",
                "hx-trigger": "change",
                "hx-target": "#project_list",
                "hx-select": "#project_list",
                "hx-swap": "outerHTML",
            }
        ),
        label="Filter by Technology",
        empty_label="All",
    )
