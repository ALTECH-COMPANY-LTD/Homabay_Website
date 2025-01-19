# hr_payroll/admin_views.py

from django.contrib.admin.views.main import ChangeList
from django.http import JsonResponse
from django.utils import timezone
from .models import Attendance, Payroll, Performance

def attendance_chart_data(request):
    today = timezone.now()
    start_date = today.replace(day=1)  # Start of current month
    end_date = today.replace(day=28) + timezone.timedelta(days=4)  # End of current month
    end_date = end_date - timezone.timedelta(days=end_date.day)

    attendance_data = Attendance.objects.filter(date__range=(start_date, end_date))
    chart_data = {
        'dates': [],
        'present': [],
        'absent': []
    }

    for day in range(1, end_date.day + 1):
        date = start_date.replace(day=day)
        chart_data['dates'].append(date.strftime('%Y-%m-%d'))
        present_count = attendance_data.filter(date=date, is_absent=False).count()
        absent_count = attendance_data.filter(date=date, is_absent=True).count()
        chart_data['present'].append(present_count)
        chart_data['absent'].append(absent_count)
    
    return JsonResponse(chart_data)

def payroll_chart_data(request):
    today = timezone.now()
    start_date = today.replace(day=1)  # Start of current month
    end_date = today.replace(day=28) + timezone.timedelta(days=4)  # End of current month
    end_date = end_date - timezone.timedelta(days=end_date.day)

    payroll_data = Payroll.objects.filter(date__range=(start_date, end_date))
    chart_data = {
        'dates': [],
        'total_salary': []
    }

    for day in range(1, end_date.day + 1):
        date = start_date.replace(day=day)
        chart_data['dates'].append(date.strftime('%Y-%m-%d'))
        total_salary = payroll_data.filter(date=date).aggregate(Sum('total_salary'))['total_salary__sum'] or 0
        chart_data['total_salary'].append(total_salary)

    return JsonResponse(chart_data)

def performance_chart_data(request):
    today = timezone.now()
    start_date = today.replace(day=1)  # Start of current month
    end_date = today.replace(day=28) + timezone.timedelta(days=4)  # End of current month
    end_date = end_date - timezone.timedelta(days=end_date.day)

    performance_data = Performance.objects.filter(date__range=(start_date, end_date))
    chart_data = {
        'dates': [],
        'scores': []
    }

    for day in range(1, end_date.day + 1):
        date = start_date.replace(day=day)
        chart_data['dates'].append(date.strftime('%Y-%m-%d'))
        score = performance_data.filter(date=date).aggregate(Avg('score'))['score__avg'] or 0
        chart_data['scores'].append(score)

    return JsonResponse(chart_data)