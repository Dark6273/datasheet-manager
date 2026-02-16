"""Todo admin configuration."""

from django.contrib import admin

from .models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """Admin customization for todo items."""

    list_display = ("title", "project", "status", "priority", "due_date", "updated_at")
    list_filter = ("status", "priority", "due_date", "project")
    search_fields = ("title", "details", "project__name")
    ordering = ("-created_at",)
