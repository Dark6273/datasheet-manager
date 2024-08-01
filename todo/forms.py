from django import forms
from .models import Todo

class TodoForm(forms.Form):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed', 'due_date', 'project',]
        widget = {'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}), }

    def save(self, commit):
        pass

