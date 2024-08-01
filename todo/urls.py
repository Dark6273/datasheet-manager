from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('todo/create/<int:project_id>/', views.todo_create, name='todo_create_for_project'),
    path('assign_project/<int:todo_id>/', views.todo_assign_project, name='todo_assign_project'),
]