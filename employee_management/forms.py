from django import forms
from django.contrib.auth.models import User
from .models import *

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        employee = super().save(commit=False)
        employee.user = user
        if commit:
            employee.save()
        return employee

class LeaveForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=True)

    class Meta:
        model = Leave
        exclude = ['employee', 'status', 'approved_by', 'created_at', 'updated_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ['created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in': forms.TimeInput(attrs={'type': 'time'}),
            'check_out': forms.TimeInput(attrs={'type': 'time'}),
        }

class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        exclude = ['created_at']
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ['uploaded_at']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        exclude = ['created_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        exclude = ['created_at']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'description', 'salary_range_min', 'salary_range_max']