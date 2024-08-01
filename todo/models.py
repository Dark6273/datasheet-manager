from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='todos', blank=True, null=True)

    def __str__(self):
        return self.title