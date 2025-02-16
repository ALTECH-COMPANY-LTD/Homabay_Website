# Generated by Django 5.1.4 on 2025-02-14 09:25

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
                ('category', models.CharField(choices=[('concrete_blocks', 'Concrete Blocks: Hollow blocks for versatile construction.'), ('drainage_solutions', 'Drainage Solutions: Invert blocks, shallow drains, road kerbs, channels, etc.'), ('landscaping_products', 'Landscaping Products: Paving slabs, side slabs, quadrants, and wall copings.'), ('manhole_components', 'Manhole Components: Rings, covers, cover slabs, and tapers.'), ('custom_pavers', 'Custom Pavers: Decorative and functional paving options.')], max_length=100)),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
    ]
