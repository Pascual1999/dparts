# Generated by Django 5.1.3 on 2024-12-03 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_payment_note_alter_order_proof_of_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_note',
            field=models.TextField(blank=True, null=True, verbose_name='Nota de pago'),
        ),
    ]
