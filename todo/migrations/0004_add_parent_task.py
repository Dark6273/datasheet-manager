"""Add parent task relation for subtasks."""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Add self-referential parent field to todo items."""

    dependencies = [
        ("todo", "0003_add_project"),
    ]

    operations = [
        migrations.AddField(
            model_name="todoitem",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subtasks",
                to="todo.todoitem",
            ),
        ),
    ]
