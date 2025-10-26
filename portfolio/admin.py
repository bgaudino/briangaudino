from django.contrib import admin

from admin_ordering.admin import OrderableAdmin

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


@admin.register(models.Education)
class EducationAdmin(PublishableAdmin):
    list_display = ["institution", "degree", "start_date", "end_date"]


@admin.register(models.Job)
class JobAdmin(PublishableAdmin):
    list_display = ["company", "title", "date_started", "date_ended"]
