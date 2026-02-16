"""Timer application URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.timer_view, name="timer-view"),
    path("export/", views.export_to_excel, name="export-view"),
    path("performance/", views.performance_view, name="performance"),
]
