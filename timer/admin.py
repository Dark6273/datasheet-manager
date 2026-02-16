"""Timer admin configuration."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django.utils.timesince import timesince
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)

from . import models

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Admin configuration for users."""

    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Admin configuration for groups."""

    pass


@admin.register(models.Tag)
class TagAdmin(ModelAdmin):
    """Admin configuration for tags."""

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


class TimerRecordInline(TabularInline):
    """Inline display of timer records."""

    model = models.TimerRecord
    extra = 0
    fields = ("task", "time", "created_at")
    readonly_fields = ("created_at",)
    can_delete = True
    show_change_link = True


@admin.register(models.Project)
class ProjectAdmin(ModelAdmin):
    """Admin configuration for projects."""

    list_display = (
        "name",
        "tag_display",
        "description_short",
        "status_display",
        "record_count",
    )
    list_filter = ("status", "tag")
    search_fields = ("name", "description", "tag__name")
    ordering = ("name",)
    inlines = [TimerRecordInline]
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "tag", "status"),
            },
        ),
        (
            "Information",
            {
                "fields": ("description",),
                "classes": ("collapse",),
            },
        ),
    )

    def tag_display(self, obj):
        """Render tag badge."""
        return format_html('<span class="badge badge-primary">{}</span>', obj.tag.name)

    tag_display.short_description = "label"

    def status_display(self, obj):
        """Render active status badge."""
        if obj.status:
            return format_html('<span class="badge badge-success">Active</span>')
        return format_html('<span class="badge badge-danger">Deactive</span>')

    status_display.short_description = "Status"

    def description_short(self, obj):
        """Return a truncated description."""
        if obj.description:
            return (
                obj.description[:50] + "..."
                if len(obj.description) > 50
                else obj.description
            )
        return "-"

    description_short.short_description = "Description"

    def record_count(self, obj):
        """Return count of records for the project."""
        count = obj.timerrecord_set.count()
        return format_html('<span class="badge badge-info">{}</span>', count)

    record_count.short_description = "Record count"


@admin.register(models.TimerRecord)
class TimerRecordAdmin(ModelAdmin):
    """Admin configuration for timer records."""

    list_display = (
        "task_short",
        "project_name",
        "tag_name",
        "formatted_time",
        "formatted_created_at",
    )
    list_filter = ("project", "project__tag", "created_at")
    search_fields = ("task", "project__name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": ("task", "time", "project"),
            },
        ),
        (
            "Time details",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at",)

    def task_short(self, obj):
        """Return a truncated task."""
        return obj.task[:50] + "..." if len(obj.task) > 50 else obj.task

    task_short.short_description = "Task"

    def project_name(self, obj):
        """Render project link."""
        return format_html(
            '<a href="{}">{}</a>',
            f"/admin/your_app_name/project/{obj.project.id}/change/",
            obj.project.name,
        )

    project_name.short_description = "Project"

    def tag_name(self, obj):
        """Render tag badge."""
        return format_html(
            '<span class="badge badge-primary">{}</span>', obj.project.tag.name
        )

    tag_name.short_description = "Label"

    def formatted_time(self, obj):
        """Format duration as HH:MM:SS."""
        total_seconds = int(obj.time.total_seconds())
        hours = total_seconds // 3600
        remainder = total_seconds % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        string = f'<span class="badge badge-secondary">{hours:02}:{minutes:02}:{seconds:02}</span>'
        return format_html(string)

    formatted_time.short_description = "Time"

    def formatted_created_at(self, obj):
        """Return the created date."""
        return obj.created_at.date()

    formatted_created_at.short_description = "Created at"
