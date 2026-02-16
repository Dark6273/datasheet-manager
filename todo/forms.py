"""Todo application forms."""

from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import TodoItem


class TodoItemForm(forms.ModelForm):
    """Form for creating todo items."""

    class Meta:
        model = TodoItem
        fields = ["title", "details", "project", "priority", "due_date"]
        widgets = {
            "details": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form widgets and constraints."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "field")
        self.fields["title"].widget.attrs.setdefault("placeholder", "Task title")
        self.fields["details"].widget.attrs.setdefault(
            "placeholder", "What needs to be done?"
        )

        now = timezone.localtime()
        min_value = now.replace(second=0, microsecond=0)
        max_value = min_value + timedelta(days=365)
        self.fields["due_date"].widget.attrs["min"] = min_value.isoformat(
            timespec="minutes"
        )
        self.fields["due_date"].widget.attrs["max"] = max_value.isoformat(
            timespec="minutes"
        )

    def clean_due_date(self):
        """Validate that due date is not in the past."""
        due_date = self.cleaned_data.get("due_date")
        if not due_date:
            return due_date
        if due_date < timezone.localtime():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
