# production/models.py
from django.db import models
from django.forms import ValidationError
from employee_management.models import Employee  # Update the import to use Employee from employee_management

class ProductionLine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_current_efficiency(self):
        completed_runs = self.productionrun_set.filter(status='completed')
        if completed_runs.exists():
            total_actual_output = sum(run.actual_output for run in completed_runs)
            total_target_output = sum(run.target_output for run in completed_runs)
            if total_target_output > 0:
                return (total_actual_output / total_target_output) * 100
        return 0

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError('Capacity must be greater than zero')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Production Line"
        verbose_name_plural = "Production Lines"

class ProductionRun(models.Model):
    STATUS_CHOICES = (
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    target_output = models.PositiveIntegerField()
    actual_output = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='supervised_runs')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def efficiency(self):
        if self.actual_output is not None and self.target_output > 0:
            return (self.actual_output / self.target_output) * 100
        return 0

    @property
    def duration(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None

    def clean(self):
        if self.end_time and self.start_time and self.end_time < self.start_time:
            raise ValidationError('End time must be after start time')
        if self.status == 'completed' and not self.actual_output:
            raise ValidationError('Completed runs must have actual output')

    def __str__(self):
        return f"{self.production_line.name} - {self.status}"

    class Meta:
        ordering = ['-start_time']
        verbose_name = "Production Run"
        verbose_name_plural = "Production Runs"

class ProductionOutput(models.Model):
    production_run = models.ForeignKey(ProductionRun, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Must be positive
    rejects = models.PositiveIntegerField(default=0)  # Must be positive
    reject_reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rejects < 0:
            raise ValidationError('Rejects must be non-negative')

    def __str__(self):
        return f"{self.quantity} units - {self.production_run}"

    class Meta:
        ordering = ['timestamp']  # Orders outputs by timestamp
        verbose_name = "Production Output"
        verbose_name_plural = "Production Outputs"

class RawMaterialRequirement(models.Model):
    production_run = models.ForeignKey(ProductionRun, on_delete=models.CASCADE)
    material = models.ForeignKey('inventory.RawMaterial', on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.quantity_required <= 0:
            raise ValidationError('Quantity required must be greater than zero')

    def __str__(self):
        return f"{self.quantity_required} of {self.material} for {self.production_run}"

    class Meta:
        ordering = ['material']  # Orders requirements by material
        verbose_name = "Raw Material Requirement"
        verbose_name_plural = "Raw Material Requirements"