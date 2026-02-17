"""Todo application URL configuration."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.todo_list, name="todo-list"),
    path("search/", views.todo_search, name="todo-search"),
    path("<int:item_id>/worklogs/", views.worklog_list, name="todo-worklogs"),
    path(
        "<int:item_id>/worklogs/add/",
        views.add_worklog,
        name="todo-worklogs-add",
    ),
    path("<int:item_id>/status/<str:status>/", views.update_status, name="todo-update"),
    path("<int:item_id>/delete/", views.delete_item, name="todo-delete"),
]
