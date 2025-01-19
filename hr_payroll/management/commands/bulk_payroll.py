from django.core.management.base import BaseCommand
from hr_payroll.models import Payroll, Employee
from django.utils import timezone

class Command(BaseCommand):
    help = 'Bulk process payroll for all employees'

    def handle(self, *args, **kwargs):
        today = timezone.now()
        employees = Employee.objects.all()
        
        for employee in employees:
            payroll = Payroll(employee=employee, date=today)
            payroll.hours_worked = 160  # Default hours worked
            payroll.overtime_hours = 0  # Adjust as necessary
            payroll.save()

        self.stdout.write(self.style.SUCCESS('Successfully processed payroll for all employees.'))