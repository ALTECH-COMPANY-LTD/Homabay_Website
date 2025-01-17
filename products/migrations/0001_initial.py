# Generated by Django 5.1.3 on 2024-12-02 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('dimensions', models.CharField(max_length=100)),
                ('features', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
    ]
