# Generated by Django 5.1.3 on 2025-01-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_payroll', '0003_attendance_comments_attendance_is_late_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='total_absences',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='payroll',
            unique_together={('employee', 'date')},
        ),
    ]