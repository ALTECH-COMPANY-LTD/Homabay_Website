from django.core.management.base import BaseCommand
from hr_payroll.models import Payroll, PayrollReport
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate monthly payroll report'

    def handle(self, *args, **kwargs):
        today = timezone.now()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=1) + timedelta(days=31)
        last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)

        total_salary = Payroll.objects.filter(date__gte=first_day_of_month, date__lte=last_day_of_month).aggregate(Sum('total_salary'))['total_salary__sum'] or 0

        payroll_report = PayrollReport(month=today, total_salary_paid=total_salary)
        payroll_report.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated payroll report for %s' % today.strftime('%B %Y')))