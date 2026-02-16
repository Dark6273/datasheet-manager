"""Add project relation to todo items."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Add project foreign key to todo items."""

    dependencies = [
        ("todo", "0002_update_due_date"),
        ("timer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todoitem",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="todo_items",
                to="timer.project",
            ),
        ),
    ]
