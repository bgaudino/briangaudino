from django.db import models

from admin_ordering.models import OrderableModel


class Job(models.Model):
    title = models.CharField()
    company = models.CharField()
    location = models.CharField()
    description = models.TextField()
    date_started = models.DateField()
    date_ended = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-date_started"]

    def __str__(self):
        return f"{self.title} at {self.company} ({self.location})"


class Education(models.Model):
    institution = models.CharField()
    degree = models.CharField()
    field_of_study = models.CharField()
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"


class Skill(OrderableModel):
    name = models.CharField()
    proficiency = models.CharField()

    def __str__(self):
        return f"{self.name} ({self.proficiency})"


class Project(OrderableModel):
    name = models.CharField(unique=True)
    description = models.TextField()
    url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    image = models.CharField(blank=True)
    technologies = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


class Interest(OrderableModel):
    name = models.CharField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
