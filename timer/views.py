from django.shortcuts import render
from django.http import HttpResponse
from .forms import TimerForm
from .models import TimerRecord, Project


def timer_view(request):
    if request.method == 'POST':
        form = TimerForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors.as_ul())
        
    form = TimerForm()
    records = TimerRecord.objects.all().order_by('-created_at')[:100]
    return render(request, 'timer.html', {'form': form, 'records': records})

