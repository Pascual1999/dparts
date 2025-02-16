# Generated by Django 5.1.3 on 2024-11-16 01:44

import django.db.models.deletion
import orders.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('product', '0004_alter_product_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_note',
            field=models.TextField(null=True, verbose_name='Nota de pago'),
        ),
        migrations.AlterField(
            model_name='order',
            name='proof_of_payment',
            field=models.ImageField(null=True, upload_to=orders.models.upload_to, verbose_name='Captura'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Orden'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(verbose_name='Cantidad'),
        ),
    ]
