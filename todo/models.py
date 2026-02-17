"""Todo application models."""

from django.db import models
from django.utils import timezone

from timer.models import Project


class TodoItem(models.Model):
    """Represents a single todo item with status and priority."""

    class Status(models.TextChoices):
        """Workflow status options."""

        TODO = "todo", "Todo"
        DOING = "doing", "Doing"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        """Priority options."""

        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="todo_items",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subtasks",
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.TODO
    )
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Return a readable label for admin and logs."""
        return f"{self.title}"

    @property
    def is_overdue(self) -> bool:
        """Return True when the item is overdue."""
        if not self.due_date:
            return False
        return self.due_date < timezone.localtime()

    @property
    def parent_title(self) -> str:
        """Return parent task title for UI."""
        if not self.parent:
            return ""
        return self.parent.title

    @property
    def subtask_titles(self) -> str:
        """Return child task titles as a readable string."""
        children = self.subtasks.all()
        if not children:
            return ""
        return " | ".join(child.title for child in children)
