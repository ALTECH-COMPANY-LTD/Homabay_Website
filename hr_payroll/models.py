from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class JobPosition(models.Model):
    title = models.CharField(max_length=100)
    responsibilities = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class LeaveType(models.Model):
    name = models.CharField(max_length=50)
    leave_days_allowed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2)
    leaves_per_year = models.PositiveIntegerField(default=12)
    leaves_taken = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.job_position})"

    def remaining_leaves(self):
        return self.leaves_per_year - self.leaves_taken

class SalaryHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateField()

    def __str__(self):
        return f"{self.salary} for {self.employee} (Effective from {self.effective_date})"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    hours_present = models.PositiveIntegerField(default=0)
    is_absent = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def clean(self):
        if self.hours_present < 0:
            raise ValidationError("Hours present cannot be negative.")
        if self.is_absent and self.hours_present > 0:
            raise ValidationError("An employee cannot be absent and have hours present at the same time.")

    def __str__(self):
        return f"{self.employee} - {self.date} (Hours: {self.hours_present})"

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")
        if self.employee.remaining_leaves() < (self.end_date - self.start_date).days + 1:
            raise ValidationError("Not enough leave days available.")

    def __str__(self):
        return f"{self.leave_type} request from {self.employee} ({self.start_date} to {self.end_date})"

class Deduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.amount} deducted from {self.employee} for {self.reason}"

class Overtime(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hours = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.hours} hours of overtime for {self.employee} on {self.date}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    hours_worked = models.PositiveIntegerField(default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_leaves_taken = models.PositiveIntegerField(default=0)
    total_absences = models.PositiveIntegerField(default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    class Meta:
        unique_together = ('employee', 'date')

    def get_total_hours_worked(self):
        total_hours = Attendance.objects.filter(employee=self.employee, date=self.date).aggregate(total=Sum('hours_present'))['total'] or 0
        return total_hours

    def calculate_salary(self):
        total_salary = (self.hours_worked * self.employee.hourly_rate)

        overtime_hours = Overtime.objects.filter(employee=self.employee, date=self.date).aggregate(total=Sum('hours'))['total'] or 0
        total_salary += overtime_hours * self.employee.overtime_rate

        total_deductions = Deduction.objects.filter(employee=self.employee).aggregate(total=Sum('amount'))['total'] or 0
        self.deductions = total_deductions

        leave_days = LeaveRequest.objects.filter(employee=self.employee, approved=True).count()
        total_salary -= leave_days * (self.employee.salary / 30)

        return total_salary

    def calculate_net_salary(self):
        return self.total_salary + self.bonuses - self.deductions

    def count_absences(self):
        return Attendance.objects.filter(
            employee=self.employee,
            date__month=self.date.month,
            date__year=self.date.year,
            is_absent=True
        ).count()

    def save(self, *args, **kwargs):
        if self.pk is None and Payroll.objects.filter(employee=self.employee, status='Pending').exists():
            raise ValidationError("An employee can only have one active payroll at a time.")
        
        self.hours_worked = self.get_total_hours_worked()
        self.total_leaves_taken = LeaveRequest.objects.filter(employee=self.employee, approved=True).count()
        self.total_absences = self.count_absences()
        self.total_salary = self.calculate_salary()
        self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)

    def create_new_payroll(self):
        next_month = self.date.replace(day=1) + timezone.timedelta(days=31)
        next_month = next_month.replace(day=1)  # Go to the first day of the next month
        new_payroll = Payroll(
            employee=self.employee,
            date=next_month,
            status='Pending'
        )
        new_payroll.save()

    def archive_payroll(self):
        ArchivedPayroll.objects.create(
            employee=self.employee,
            date=self.date,
            hours_worked=self.hours_worked,
            total_salary=self.total_salary,
            total_leaves_taken=self.total_leaves_taken,
            total_absences=self.total_absences,
            bonuses=self.bonuses,
            deductions=self.deductions,
            net_salary=self.net_salary,
            status=self.status,
        )

    def __str__(self):
        return f"Payroll for {self.employee} on {self.date}"

class ArchivedPayroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours_worked = models.PositiveIntegerField(default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_leaves_taken = models.PositiveIntegerField(default=0)
    total_absences = models.PositiveIntegerField(default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Archived Payroll for {self.employee} on {self.date}"

class SalaryPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank', 'Bank'),
        ('Cash', 'Cash'),
        ('Mpesa', 'Mpesa'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_payments')
    payroll = models.OneToOneField(Payroll, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.payroll:
            self.balance_due = self.payroll.net_salary - self.amount_paid
            if self.balance_due <= 0:
                self.payroll.status = 'Completed'
                self.payroll.archive_payroll()  # Archive the payroll before marking as completed
                self.payroll.create_new_payroll()  # Create new payroll for the next cycle
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.employee} on {self.payment_date} - Status: {self.status}"

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_date = models.DateField(default=timezone.now)
    score = models.IntegerField()
    feedback = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Performance review for {self.employee} on {self.review_date} - Score: {self.score}"

class Training(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training_name = models.CharField(max_length=200)
    completion_date = models.DateField()
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Training: {self.training_name} for {self.employee} - Completed on {self.completion_date}"

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.employee} - Uploaded on {self.upload_date}"

class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.employee} on {self.date_created} - Read: {self.is_read}"

class PayrollReport(models.Model):
    month = models.DateField()
    total_salary_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payroll report for {self.month.strftime('%B %Y')} - Total: {self.total_salary_paid}"

    @classmethod
    def create_report(cls, month):
        total_salary = Payroll.objects.filter(date__month=month.month, date__year=month.year).aggregate(Sum('net_salary'))['net_salary__sum'] or 0
        report = cls(month=month, total_salary_paid=total_salary)
        report.save()
        return report