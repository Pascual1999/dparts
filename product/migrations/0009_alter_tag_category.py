# Generated by Django 5.1.3 on 2025-01-15 01:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='Category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='product.category', verbose_name='Categoría'),
        ),
    ]
