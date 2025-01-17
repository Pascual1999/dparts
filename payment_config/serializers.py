from rest_framework import serializers

from .models import PaymentMethod, DollarExchangeHistory


class DollarExchangeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DollarExchangeHistory
        fields = (
            'date',
            'value',
            'page'
        )


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = (
            'id',
            'name',
            'payment_data'
        )

