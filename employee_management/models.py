# employee_management/models.py
from django.db import models
from accounts.models import CustomUser  # Import your CustomUser model
from django.core.validators import MinValueValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.department}"

class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    MARITAL_STATUS = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Use CustomUser here
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS)
    blood_group = models.CharField(max_length=5, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    date_joined = models.DateField()
    profile_picture = models.ImageField(upload_to='employee_photos/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='present')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['employee', 'date']

class Leave(models.Model):
    LEAVE_TYPES = (
        ('AL', 'Annual Leave'),
        ('SL', 'Sick Leave'),
        ('ML', 'Maternity Leave'),
        ('PL', 'Paternity Leave'),
        ('UL', 'Unpaid Leave'),
    )
    
    LEAVE_STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=1, choices=LEAVE_STATUS, default='P')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # Use CustomUser here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_period = models.CharField(max_length=50)
    review_date = models.DateField()
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    productivity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    teamwork = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField()
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  # Use CustomUser here
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    document_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

class Training(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    trainer = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(Employee, through='TrainingParticipant')
    status = models.CharField(max_length=20, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

class TrainingParticipant(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='enrolled')
    completion_date = models.DateField(null=True, blank=True)
    certificate_issued = models.BooleanField(default=False)

class Shift(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)

class EmployeeShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default='scheduled')