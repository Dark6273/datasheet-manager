from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.name}"
    

class TimerRecord(models.Model):
    task = models.TextField(null=False)
    time = models.DurationField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.task} - {self.project}:{self.project.tag} - {self.time}"
