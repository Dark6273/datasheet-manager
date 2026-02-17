"""Add work log entries for todo items."""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Create work log model."""

    dependencies = [
        ("todo", "0004_add_parent_task"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.TextField(blank=True)),
                ("duration_minutes", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "todo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worklogs",
                        to="todo.todoitem",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
