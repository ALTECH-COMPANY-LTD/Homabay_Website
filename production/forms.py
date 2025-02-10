# forms.py
from django import forms
from .models import ProductionLine, ProductionRun, ProductionOutput, RawMaterialRequirement

class ProductionLineForm(forms.ModelForm):
    class Meta:
        model = ProductionLine
        fields = ['name', 'description', 'capacity', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProductionRunForm(forms.ModelForm):
    class Meta:
        model = ProductionRun
        fields = ['production_line', 'start_time', 'end_time', 'target_output', 
                 'actual_output', 'status', 'supervisor', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        status = cleaned_data.get('status')

        if end_time and start_time and end_time < start_time:
            raise forms.ValidationError('End time must be after start time')
        
        if status == 'completed' and not cleaned_data.get('actual_output'):
            raise forms.ValidationError('Completed runs must have actual output')

        return cleaned_data

class ProductionOutputForm(forms.ModelForm):
    class Meta:
        model = ProductionOutput
        fields = ['production_run', 'quantity', 'rejects', 'reject_reason']
        widgets = {
            'reject_reason': forms.Textarea(attrs={'rows': 3}),
        }

class RawMaterialRequirementForm(forms.ModelForm):
    class Meta:
        model = RawMaterialRequirement
        fields = ['production_run', 'material', 'quantity_required']