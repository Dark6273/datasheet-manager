"""Timer application views."""

import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import make_naive
from django_jalali.forms import jDateField
from jdatetime import datetime as jdatetime
from jdatetime import timedelta

from .forms import ExportForm, TimerForm
from .models import Project, Tag, TimerRecord


def format_timedelta(td):
    """Format a timedelta as HH:MM:SS."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def extract_timesheet(
    start_time: jDateField,
    end_time: jDateField,
    project: Project | None,
    tag: Tag | None,
):
    """Extract timesheet data into a pandas dataframe."""
    query = Q(created_at__gte=start_time) & Q(
        created_at__lte=end_time + timedelta(days=1)
    )

    if tag:
        query &= Q(project__tag=tag)
    if project:
        query &= Q(project=project)

    records = TimerRecord.objects.filter(query).values(
        "task", "time", "project__name", "created_at"
    )

    if len(records) <= 0:
        return

    df = pd.DataFrame(list(records))
    df["created_at"] = df["created_at"].apply(lambda x: make_naive(x))
    all_duration_time = format_timedelta(df["time"].sum())
    df["time"] = df["time"].apply(lambda x: format_timedelta(x))

    sum_row = pd.DataFrame([{"task": "sum", "time": all_duration_time}])
    df = pd.concat([df, sum_row], ignore_index=True)

    return df


def timer_view(request):
    """Render the timer page and handle time entry creation."""
    if request.method == "POST":
        form = TimerForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors.as_ul())

    form = TimerForm()
    export_form = ExportForm()
    records = TimerRecord.objects.all().order_by("-created_at")[:25]
    return render(
        request,
        "timer.html",
        {"form": form, "export_form": export_form, "records": records},
    )


def export_to_excel(request):
    """Export filtered timesheet data as CSV or Excel."""
    if request.method != "POST":
        return Http404()

    form = ExportForm(request.POST)

    if not form.is_valid():
        # return HttpResponse("<h1>Bad request</h1>", status=400)
        return HttpResponse(form.errors.as_ul())

    cleaned_data = form.cleaned_data
    df = extract_timesheet(
        cleaned_data["start_date"],
        cleaned_data["end_date"],
        cleaned_data["project_name"],
        cleaned_data["project_tag"],
    )

    if df is None:
        return HttpResponse(
            "<h1>Timesheet is Null</h1><br/><a href='/'>back to timer</a>"
        )

    if cleaned_data["export_format"] == "excel":
        # Export Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=my_data.xlsx"

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")
    else:
        # export CSV
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=my_data.csv"

        df.to_csv(response, index=False)

    return response


@staff_member_required
def performance_view(request):
    """Render the performance dashboard for daily and monthly summaries."""
    today = jdatetime.fromgregorian(datetime=timezone.now())
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    today_gregorian = today.togregorian()
    month_start_gregorian = month_start.togregorian()

    daily_records = TimerRecord.objects.filter(created_at__date=today_gregorian.date())
    daily_total_time = (
        daily_records.aggregate(total=Sum("time"))["total"] or timedelta()
    )
    daily_project_times = daily_records.values("project__name").annotate(
        total=Sum("time")
    )

    monthly_records = TimerRecord.objects.filter(
        created_at__gte=month_start_gregorian, created_at__lte=today_gregorian
    )
    monthly_total_time = (
        monthly_records.aggregate(total=Sum("time"))["total"] or timedelta()
    )
    monthly_project_times = monthly_records.values("project__name").annotate(
        total=Sum("time")
    )

    context = {
        "daily_total_time": format_timedelta(daily_total_time),
        "daily_project_times": [
            (item["project__name"], item["total"] or timedelta())
            for item in daily_project_times
        ],
        "monthly_total_time": format_timedelta(monthly_total_time),
        "monthly_project_times": [
            (item["project__name"], item["total"] or timedelta())
            for item in monthly_project_times
        ],
    }
    return render(request, "performance.html", context)
