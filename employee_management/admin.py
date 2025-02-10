from django.contrib import admin
from .models import *

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'department', 'position', 'phone', 'is_active')
    list_filter = ('department', 'is_active', 'gender', 'date_joined')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'phone')
    ordering = ('-date_joined',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'salary_range_min', 'salary_range_max')
    list_filter = ('department',)
    search_fields = ('title', 'department__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('date', 'status')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'date'

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'start_date'

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payment_date', 'basic_salary', 'net_salary', 'payment_status')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'payment_date'

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_period', 'review_date', 'productivity', 'reviewed_by')
    list_filter = ('review_date',)
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'review_date'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'document_type', 'uploaded_at', 'expiry_date')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'title')
    date_hierarchy = 'uploaded_at'

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'trainer', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'trainer')
    date_hierarchy = 'start_date'

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name',)

admin.site.register(TrainingParticipant)
admin.site.register(EmployeeShift)