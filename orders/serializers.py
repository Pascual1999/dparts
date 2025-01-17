from rest_framework import serializers

from payment_config.models import PaymentMethod
from product.serializers import ProductSerializer

from .models import Order, OrderItem


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'price',
            'product',
            'quantity'
        )


class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
                'id',
                'shipping_address',
                'contact_number',
                'status',
                'amount',
                'amount_VEF',
                'items',
                'created_at',
                'updated_at',
        )


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            'price',
            'product',
            'quantity'
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
                'id',
                'shipping_address',
                'contact_number',
                'status',
                'IVA',
                'exchange_rate',
                'amount',
                'amount_VEF',
                'items',
                'payment_method',
                'proof_of_payment'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'required': False},
            'IVA': {'required': False},
            'exchange_rate': {'required': False},
            'amount': {'required': False},
            'amount_VEF': {'required': False},
            'payment_method': {'required': False},
            'proof_of_payment': {'required': False}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data)

        return order

    def update(self, instance, validated_data):
        instance.shipping_address = validated_data.get(
            'shipping_address', instance.shipping_address
            )
        instance.contact_number = validated_data.get(
            'contact_number', instance.contact_number
            )
        instance.status = validated_data.get(
            'status', instance.status
            )
        instance.amount = validated_data.get(
            'amount', instance.amount
            )
        instance.payment_method = validated_data.get(
            'payment_method', instance.payment_method
            )
        instance.proof_of_payment = validated_data.get(
            'proof_of_payment', instance.proof_of_payment
            )
        instance.save()
        # Los articulos no pueden ser actualizados a traves de este serializer.

        return instance

