from datetime import timedelta

from django import forms
from .models import TimerRecord


class TimerForm(forms.ModelForm):
    class Meta:
        model = TimerRecord
        fields = ['task', 'time', 'project']
    
    def clean_time(self):
        time = self.cleaned_data.get('time') // 1000

        if time == timedelta(seconds=0):
            raise forms.ValidationError("زمان نمی‌تواند صفر باشد")

        return time

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget = forms.HiddenInput()

        self.fields['project'].widget.attrs['class'] = "form-control"
        self.fields['task'].widget.attrs['class'] = "form-control"
        self.fields['task'].widget.attrs['rows'] = 1
