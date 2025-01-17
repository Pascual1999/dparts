from rest_framework import serializers

from .models import Category, Product, Tag


class SimpleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'get_absolute_url',
        )


class ProductSerializer(serializers.ModelSerializer):
    tags = SimpleTagSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'get_absolute_url',
            'sku',
            'brand',
            'description',
            'price',
            'get_image',
            'get_thumbnail',
            'tags'
        )
    

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'products'
        )

    def get_products(self, obj):
        return ProductSerializer(
            obj.products.filter(is_active=True).order_by('id'), 
            many=True).data


class TagSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'products',
            'get_absolute_url',
        )
