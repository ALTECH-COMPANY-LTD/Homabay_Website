# Generated by Django 5.1.4 on 2025-02-14 09:25

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=50, unique=True)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_delivery', models.DateField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending Approval'), ('approved', 'Approved'), ('ordered', 'Ordered'), ('partially_received', 'Partially Received'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('quantity_available', models.FloatField()),
                ('reorder_level', models.FloatField()),
                ('cost_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_person', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('tax_number', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialReceiving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiving_number', models.CharField(max_length=50, unique=True)),
                ('receiving_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('received_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.purchaseorder')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('received_quantity', models.FloatField(default=0)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.purchaseorder')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialReceivingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)])),
                ('notes', models.TextField(blank=True)),
                ('receiving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.materialreceiving')),
                ('purchase_order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.purchaseorderitem')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('transaction_type', models.CharField(choices=[('in', 'In'), ('out', 'Out')], max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reference', models.CharField(max_length=100)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterial')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier'),
        ),
    ]
