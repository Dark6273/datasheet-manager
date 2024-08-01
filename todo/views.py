from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo, Project
from .forms import TodoForm
from django.http import JsonResponse


def todo_list(request):
    todos = Todo.objects.all()
    context = {
        'todo': todos,
    }
    return render(request, 'todo_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    todos = project.todos.all()
    return render(request, 'project_detail.html', {'project': project, 'todos': todos})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


def todo_create(request, project_id=None):
    project = get_object_or_404(Project, pk=project_id) if project_id else None

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            if todo is None:
                print("Error: Form save returned None")
            else:
                print(f"Form is valid. Todo object: {todo}")
                if project:
                    todo.project = project
                todo.save()
                if request.is_ajax():
                    return JsonResponse({'success': True})
                if project:
                    return redirect('project_detail', pk=project.pk)
                else:
                    return redirect('todo_list')
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TodoForm()

    context = {
        'form': form,
        'project': project
    }
    return render(request, 'todo_create.html', context)

def todo_assign_project(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == "POST":
        project_id = request.POST.get('project_id')
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            todo.project = project
            todo.save()
    return redirect('todo_list')