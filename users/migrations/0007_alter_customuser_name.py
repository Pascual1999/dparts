# Generated by Django 5.1.3 on 2025-02-16 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=75, verbose_name='Nombre'),
        ),
    ]
