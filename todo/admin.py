"""Todo admin configuration."""

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import TodoItem, WorkLog


class WorkLogInline(TabularInline):
    """Inline display of worklog records."""

    model = WorkLog
    extra = 0
    fields = ("note", "duration_minutes", "created_at")
    readonly_fields = ("created_at",)
    can_delete = False
    show_change_link = False


@admin.register(TodoItem)
class TodoItemAdmin(ModelAdmin):
    """Admin customization for todo items."""

    list_display = (
        "title",
        "parent",
        "project",
        "status",
        "priority",
        "due_date",
        "updated_at",
    )
    list_filter = ("status", "priority", "due_date", "project", "parent")
    search_fields = ("title", "details", "project__name", "parent__title")
    ordering = ("-created_at",)
    inlines = [WorkLogInline]


@admin.register(WorkLog)
class WorkLogAdmin(ModelAdmin):
    """Admin customization for work logs."""

    list_display = ("todo", "duration_minutes", "created_at")
    list_filter = ("created_at",)
    search_fields = ("todo__title", "note")
    ordering = ("-created_at",)
