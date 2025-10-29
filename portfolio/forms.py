from django import forms

from portfolio.models import Contact, Technology


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }


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
