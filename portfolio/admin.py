from django.contrib import admin

from admin_ordering.admin import OrderableAdmin

from portfolio import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Project)
class ProjectAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["name", "ordering"]
    list_editable = ["ordering"]


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    pass
