from django import forms

from employee_management.models import Position
from .models import CustomUser, Employee  # Updated import

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['employee_id', 'department', 'position', 'skills', 'hire_date']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Updated to use CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Updated to use CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

