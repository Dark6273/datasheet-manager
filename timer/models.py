"""Timer application models."""

from django.db import models
from django_jalali.db import models as jmodels


class Tag(models.Model):
    """Tag for grouping projects."""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return tag name."""
        return str(self.name)


class Project(models.Model):
    """Project definition for time tracking."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    def __str__(self) -> str:
        """Return project name."""
        return f"{self.name}"


class TimerRecord(models.Model):
    """A time entry recorded against a project."""

    task = models.TextField(null=False)
    time = models.DurationField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a readable summary for admin and logs."""
        return f"{self.task} - {self.project}:{self.project.tag} - {self.time}"
