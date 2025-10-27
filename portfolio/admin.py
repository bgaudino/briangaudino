from django.contrib import admin

from admin_ordering.admin import OrderableAdmin
from reverse_relationship.admin import ReverseRelationshipAdmin

from portfolio import models


class PublishableAdmin(admin.ModelAdmin):
    actions = ["publish", "unpublish"]

    @admin.action(description="Publish selected items")
    def publish(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected items")
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        return list(fields) + ["is_published"]

    def get_list_filter(self, request):
        fields = super().get_list_filter(request)
        return list(fields) + ["is_published"]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]


@admin.register(models.Project)
class ProjectAdmin(OrderableAdmin, PublishableAdmin):
    list_display = ["name", "ordering"]
    list_editable = ["ordering"]
    filter_horizontal = ["tech_stack"]
    fields = [
        "name",
        "description",
        "image",
        "url",
        "repository_url",
        "tech_stack",
        "is_published",
    ]


@admin.register(models.Education)
class EducationAdmin(PublishableAdmin):
    list_display = ["institution", "degree"]
    fields = [
        "institution",
        "degree",
        "field_of_study",
        "location",
        "start_date",
        "end_date",
        "description",
        "highlights",
        "is_published",
    ]


@admin.register(models.Job)
class JobAdmin(PublishableAdmin):
    list_display = ["company", "title"]
    fields = [
        "company",
        "title",
        "location",
        "description",
        "start_date",
        "end_date",
        "highlights",
        "is_published",
    ]


@admin.register(models.Technology)
class TechnologyAdmin(PublishableAdmin, OrderableAdmin, ReverseRelationshipAdmin):
    list_display = ["name", "proficiency", "ordering"]
    list_editable = ["proficiency", "ordering"]
    fields = [
        "name",
        "proficiency",
        "is_published",
    ]
    related_fields = ["project_set"]
    related_filter_horizontal = ["project_set"]


@admin.register(models.Content)
class ContentAdmin(PublishableAdmin):
    list_display = ["title"]
    fields = [
        "title",
        "content",
        "is_published",
    ]
