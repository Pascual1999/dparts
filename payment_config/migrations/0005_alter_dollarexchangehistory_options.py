# Generated by Django 5.1.3 on 2025-01-10 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment_config', '0004_alter_dollarexchangehistory_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dollarexchangehistory',
            options={'ordering': ['-date'], 'verbose_name': 'Tasa del dolar/historial', 'verbose_name_plural': 'Tasa del dolar/historial'},
        ),
    ]
