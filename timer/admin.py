from django.contrib import admin
from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'tag', 'status']
    list_filter = ['tag', 'status']


@admin.register(models.TimerRecord)
class TimerRecordAdmin(admin.ModelAdmin):
    list_display = ['task', 'time', 'project', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['task']
    ordering = ['-created_at']


admin.site.register(models.Tag)
