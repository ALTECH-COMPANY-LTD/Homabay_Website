# Generated by Django 5.1.4 on 2025-02-10 05:19

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('trainer', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(default='upcoming', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('marital_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('W', 'Widowed')], max_length=1)),
                ('blood_group', models.CharField(blank=True, max_length=5)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=15)),
                ('emergency_contact', models.CharField(max_length=15)),
                ('date_joined', models.DateField()),
                ('profile_picture', models.ImageField(blank=True, upload_to='employee_photos/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee_management.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('document_type', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='employee_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('AL', 'Annual Leave'), ('SL', 'Sick Leave'), ('ML', 'Maternity Leave'), ('PL', 'Paternity Leave'), ('UL', 'Unpaid Leave')], max_length=2)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_period', models.CharField(max_length=50)),
                ('review_date', models.DateField()),
                ('punctuality', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('productivity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('communication', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('teamwork', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comments', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
                ('reviewed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('salary_range_min', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salary_range_max', models.DecimalField(decimal_places=2, max_digits=10)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.department')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee_management.position'),
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('allowances', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('payment_status', models.BooleanField(default=False)),
                ('payment_method', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(default='scheduled', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.shift')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='enrolled', max_length=20)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('certificate_issued', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.training')),
            ],
        ),
        migrations.AddField(
            model_name='training',
            name='participants',
            field=models.ManyToManyField(through='employee_management.TrainingParticipant', to='employee_management.employee'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='present', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_management.employee')),
            ],
            options={
                'unique_together': {('employee', 'date')},
            },
        ),
    ]
