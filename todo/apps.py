"""Todo app configuration."""

from django.apps import AppConfig


class TodoConfig(AppConfig):
    """Application configuration for the todo app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "todo"
    verbose_name = "Todo"
