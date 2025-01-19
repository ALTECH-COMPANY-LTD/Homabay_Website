from django.contrib import admin
from .models import (
    Employee,
    Attendance,
    LeaveRequest,
    Payroll,
    LeaveType,
    PayrollReport,
    Department,
    SalaryHistory,
    JobPosition,
    PerformanceReview,
    Training,
    Document,
    Notification,
    SalaryPayment,
    Deduction,
    Overtime,
)

# Define inline classes for related models
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

class LeaveRequestInline(admin.TabularInline):
    model = LeaveRequest
    extra = 0

class PayrollInline(admin.TabularInline):
    model = Payroll
    extra = 0

class DeductionInline(admin.TabularInline):
    model = Deduction
    extra = 0

class OvertimeInline(admin.TabularInline):
    model = Overtime
    extra = 0

class PerformanceReviewInline(admin.TabularInline):
    model = PerformanceReview
    extra = 0

class TrainingInline(admin.TabularInline):
    model = Training
    extra = 0

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0

class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0

class SalaryPaymentInline(admin.TabularInline):
    model = SalaryPayment
    extra = 0

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department')

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'leave_days_allowed')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'job_position',
        'department',
        'role',
        'salary',
        'hourly_rate',
        'overtime_rate',
        'leaves_per_year',
        'leaves_taken',
        'remaining_leaves',
    )
    inlines = [
        AttendanceInline,
        LeaveRequestInline,
        PayrollInline,
        DeductionInline,
        OvertimeInline,
        PerformanceReviewInline,
        TrainingInline,
        DocumentInline,
        NotificationInline,
        SalaryPaymentInline,
    ]
    search_fields = ('first_name', 'last_name', 'user__username')

    def remaining_leaves(self, obj):
        return obj.remaining_leaves()
    remaining_leaves.short_description = 'Remaining Leaves'

@admin.register(SalaryHistory)
class SalaryHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'effective_date')
    list_filter = ('employee',)
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'hours_present', 'is_absent', 'is_late', 'comments')
    list_filter = ('employee', 'date', 'is_absent', 'is_late')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'approved')
    list_filter = ('employee', 'leave_type', 'approved')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'hours_worked', 'total_salary', 'deductions', 'net_salary', 'total_leaves_taken', 'total_absences', 'status')
    list_filter = ('employee', 'date', 'status')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('payroll', 'payment_date', 'amount_paid', 'payment_method', 'status', 'balance_due')
    list_filter = ('payment_method', 'status', 'payroll__employee')
    search_fields = ('payroll__employee__first_name', 'payroll__employee__last_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for payment in qs:
            # Ensure balance_due is updated based on net_salary
            payment.balance_due = payment.payroll.net_salary - payment.amount_paid
        return qs

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_date', 'score', 'reviewer')
    list_filter = ('employee', 'review_date')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training_name', 'completion_date')
    list_filter = ('employee',)
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'upload_date')
    list_filter = ('employee',)
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'message', 'date_created', 'is_read')
    list_filter = ('employee', 'is_read')
    search_fields = ('employee__first_name', 'employee__last_name')

@admin.register(PayrollReport)
class PayrollReportAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_salary_paid')
    list_filter = ('month',)