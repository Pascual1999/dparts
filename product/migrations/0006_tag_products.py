# Generated by Django 5.1.3 on 2024-12-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_brand_product_sku_tag_producttag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='products',
            field=models.ManyToManyField(blank=True, through='product.ProductTag', to='product.product'),
        ),
    ]
