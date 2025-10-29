from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from admin_ordering.models import OrderableModel
from django_jsonform.models.fields import ArrayField


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(models.Model):
    is_published = models.BooleanField(default=True)

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True


class Experience(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(blank=True)
    description = models.TextField(blank=True)
    highlights = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        abstract = True
        ordering = ["-start_date"]


class Job(Experience, PublishableModel):
    title = models.CharField()
    company = models.CharField()

    def __str__(self):
        return f"{self.title} at {self.company} ({self.location})"


class Education(Experience, PublishableModel):
    institution = models.CharField()
    degree = models.CharField()
    field_of_study = models.CharField()

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"


class Technology(PublishableModel, OrderableModel):
    name = models.CharField()
    proficiency = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    icon = models.CharField(blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name_plural = "Technologies"

    def __str__(self):
        return f"{self.name} ({self.proficiency})"


class Project(PublishableModel, OrderableModel):
    name = models.CharField(unique=True)
    description = models.TextField()
    url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    image = models.ImageField(blank=True)
    tech_stack = models.ManyToManyField(Technology, blank=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"


class Content(PublishableModel):
    title = models.CharField(unique=True)
    content = models.TextField()

    class Meta:
        verbose_name_plural = "Content"

    def __str__(self):
        return self.title


class PersonalInfo(PublishableModel):
    name = models.CharField()
    title = models.CharField()
    email = models.EmailField()
    phone = models.CharField(blank=True)
    summary = models.TextField(blank=True)
    street_address = models.CharField(blank=True)
    city = models.CharField(blank=True)
    state = models.CharField(blank=True)
    zip_code = models.CharField(blank=True)
    links = ArrayField(models.URLField(), default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
