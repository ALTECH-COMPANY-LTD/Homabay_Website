# Generated by Django 5.1.3 on 2025-01-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_payroll', '0002_alter_attendance_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payroll',
            name='total_leaves_taken',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
