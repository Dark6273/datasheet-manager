"""Update due_date field to DateTimeField."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Alter due_date type to include time."""

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="due_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
