# Generated by Django 5.1.3 on 2025-01-19 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_payroll', '0009_payroll_net_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedPayroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hours_worked', models.PositiveIntegerField(default=0)),
                ('total_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_leaves_taken', models.PositiveIntegerField(default=0)),
                ('total_absences', models.PositiveIntegerField(default=0)),
                ('bonuses', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_payroll.employee')),
            ],
        ),
    ]
