# Generated by Django 5.1.3 on 2025-01-10 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
