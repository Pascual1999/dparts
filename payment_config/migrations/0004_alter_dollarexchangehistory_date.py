# Generated by Django 5.1.3 on 2025-01-10 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_config', '0003_alter_dollarexchangehistory_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dollarexchangehistory',
            name='date',
            field=models.DateTimeField(verbose_name='Fecha'),
        ),
    ]
