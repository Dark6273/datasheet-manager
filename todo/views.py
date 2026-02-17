"""Todo application views."""

from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TodoItemForm
from .models import TodoItem


def _todo_queryset():
    """Return optimized queryset for todo board rendering."""
    return (
        TodoItem.objects.select_related("project", "parent")
        .prefetch_related("subtasks")
        .all()
    )


def _render_board(request: HttpRequest, queryset=None) -> HttpResponse:
    """Render the todo board fragment."""
    items = queryset or _todo_queryset()
    context = {
        "todo_items": [item for item in items if item.status == TodoItem.Status.TODO],
        "doing_items": [item for item in items if item.status == TodoItem.Status.DOING],
        "done_items": [item for item in items if item.status == TodoItem.Status.DONE],
    }
    return render(request, "todo/board.html", context)


def todo_list(request: HttpRequest) -> HttpResponse:
    """Render the todo board page and handle create requests."""
    if request.method == "POST":
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request") == "true":
                query = request.GET.get("q", "").strip()
                items = _todo_queryset()
                if query:
                    items = items.filter(
                        Q(title__icontains=query)
                        | Q(details__icontains=query)
                        | Q(project__name__icontains=query)
                    )
                return _render_board(request, queryset=items)
            return redirect("todo-list")
    else:
        form = TodoItemForm()

    query = request.GET.get("q", "").strip()
    items = _todo_queryset()
    if query:
        items = items.filter(
            Q(title__icontains=query)
            | Q(details__icontains=query)
            | Q(project__name__icontains=query)
        )
    if request.headers.get("HX-Request") == "true":
        return _render_board(request, queryset=items)
    context = {
        "form": form,
        "query": query,
        "todo_items": [item for item in items if item.status == TodoItem.Status.TODO],
        "doing_items": [item for item in items if item.status == TodoItem.Status.DOING],
        "done_items": [item for item in items if item.status == TodoItem.Status.DONE],
    }
    return render(request, "todo/list.html", context)


def todo_search(request: HttpRequest) -> HttpResponse:
    """Return filtered board results for search."""
    query = request.GET.get("q", "").strip()
    items = _todo_queryset()
    if query:
        items = items.filter(
            Q(title__icontains=query)
            | Q(details__icontains=query)
            | Q(project__name__icontains=query)
        )
    return _render_board(request, queryset=items)


@require_POST
def update_status(request: HttpRequest, item_id: int, status: str) -> HttpResponse:
    """Update a todo item status and return updated board if requested via HTMX."""
    item = get_object_or_404(TodoItem, pk=item_id)
    valid_status = {choice[0] for choice in TodoItem.Status.choices}
    if status in valid_status:
        item.status = status
        item.save(update_fields=["status", "updated_at"])
    if request.headers.get("HX-Request") == "true":
        return _render_board(request)
    return redirect("todo-list")


@require_POST
def delete_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """Delete a todo item and return updated board if requested via HTMX."""
    item = get_object_or_404(TodoItem, pk=item_id)
    item.delete()
    if request.headers.get("HX-Request") == "true":
        return _render_board(request)
    return redirect("todo-list")
