from rest_framework.generics import (ListAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from knox.auth import TokenAuthentication


from .models import PaymentConfig, PaymentMethod, DollarExchangeHistory
from .serializers import (PaymentMethodSerializer,
                          DollarExchangeHistorySerializer)


class ListPaymentMethodsView(ListAPIView):
    """
    Vista para obtener todos los metodos de pago activos

    Método: GET
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetBCVView(APIView):
    """
    Vista para obtener la ultima tasa de cambio de dolares
    registrada.

    Método: GET
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):

        ExchangeRate = DollarExchangeHistory.objects.all().order_by('-date')
        serializer = DollarExchangeHistorySerializer(ExchangeRate.first(),
                                                     many=False)
        return Response(serializer.data)
    

class GetIVAView(APIView):
    """
    Vista para obtener el IVA

    Método: GET
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):

        iva = PaymentConfig.objects.get(key='IVA').value
        return Response(iva)
    

class GetAllPaymentDataView(APIView):
    """
    Vista para obtener el iva, la tasa de cambio y los metodos de pago.

    Método: GET"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):

        iva = PaymentConfig.objects.get(key='IVA').value
        exchange_rate = DollarExchangeHistory.objects.all().order_by('-date').first().value
        payment_methods = PaymentMethod.objects.filter(is_active=True)

        iva = float(iva) / 100

        return Response({'IVA': iva,
                         'ExchangeRate': exchange_rate,
                         'PaymentMethods': PaymentMethodSerializer(
                             payment_methods,
                             many=True).data})
