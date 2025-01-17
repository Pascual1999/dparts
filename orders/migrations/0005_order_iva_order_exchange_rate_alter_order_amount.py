# Generated by Django 5.1.3 on 2025-01-10 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderitem_product_name_alter_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='IVA',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='IVA'),
        ),
        migrations.AddField(
            model_name='order',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Tasa de cambio'),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Monto (USD)'),
        ),
    ]
