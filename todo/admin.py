"""Todo admin configuration."""

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import TodoItem


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
