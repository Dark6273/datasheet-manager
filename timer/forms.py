from datetime import timedelta
from django import forms
from django.utils import timezone
from django_jalali import forms as jforms
from jalali_date.widgets import AdminJalaliDateWidget

from .models import Tag, TimerRecord, Project


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


class ExportForm(forms.Form):
    EXPORT_CHOICES = (
        ("csv", "csv"),
        ("excel", "excel")
    )

    start_date = jforms.jDateField(
        widget=AdminJalaliDateWidget(attrs={'class': 'jalali_date-date form-control', 'placeholder': "start date"}),
        label='Start date',
    )
    end_date = jforms.jDateField(
        widget=AdminJalaliDateWidget(attrs={'class': 'jalali_date-date form-control', 'placeholder': "end date"}),
        label='End date',
        # initial=timezone.now
    )
    project_name = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'project name'}),
        label='Project name',
        required=False
    )
    project_tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'tag'}),
        label='Tag',
        required=False
    )
    export_format = forms.ChoiceField(
        choices=EXPORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'export type'}),
        label="export type"
    )

    def clean(self):
        cleaned_data = super().clean()  
        project_name = cleaned_data.get('project_name')
        project_tag = cleaned_data.get('project_tag')

        if not project_name and not project_tag:
            raise forms.ValidationError('Please fill in at least one of the project name or project tag fields.')

        return cleaned_data

