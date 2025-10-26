from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from admin_ordering.models import OrderableModel


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(models.Model):
    is_published = models.BooleanField(default=True)

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True


class Job(PublishableModel):
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


class Education(PublishableModel):
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


class Skill(PublishableModel, OrderableModel):
    name = models.CharField()
    proficiency = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta(OrderableModel.Meta):
        pass

    def __str__(self):
        return f"{self.name} ({self.proficiency})"


class Project(PublishableModel, OrderableModel):
    name = models.CharField(unique=True)
    description = models.TextField()
    url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    image = models.CharField(blank=True)
    technologies = models.JSONField(default=list, blank=True)

    class Meta(OrderableModel.Meta):
        pass

    def __str__(self):
        return self.name


class Interest(PublishableModel, OrderableModel):
    name = models.CharField(unique=True)
    description = models.TextField(blank=True)

    class Meta(OrderableModel.Meta):
        pass

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
