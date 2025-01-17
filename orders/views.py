from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     UpdateAPIView, RetrieveAPIView)

from payment_config.models import (DollarExchangeHistory,
                                   PaymentConfig, PaymentMethod)

from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer

from knox.auth import TokenAuthentication


class CreateOrder(CreateAPIView):
    """
    Vista para crear una nueva orden de compra.
    
    Método: POST
    Parámetros:
        contact_number: numero de contacto
        shipping_address: direccion de envio
        items: lista de items de la orden

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Calcular el monto desde el servidor.
        IVA = float(PaymentConfig.objects.get(key='IVA').value) / 100
        exchange_rate = DollarExchangeHistory.objects.all().order_by('-date').first().value

        amount = sum(item.get('quantity') *
                     item.get('product').price
                     for item in serializer.validated_data['items'])
        amount = float(amount) * (1 + IVA)
        amount_VEF = amount * float(exchange_rate)

        serializer.save(user=self.request.user, amount=amount,
                        amount_VEF=amount_VEF,
                        IVA=IVA,
                        exchange_rate=exchange_rate,
                        status=Order.IN_PROGRESS)


class UpdateOrder(UpdateAPIView):
    """
    Vista para actualizar una orden de compra con su captura de pago.

    Método: PATCH
    Parámetros:
        payment_method: id del metodo de pago
        proof_of_payment: imagen de la comprobaciÃ³n de pago
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        assert self.request.user == serializer.instance.user
        image = self.request.FILES.get('proof_of_payment')
        payment_method_id = self.request.data.get('payment_method')
        payment_method = PaymentMethod.objects.get(id=payment_method_id)
        serializer.save(
            payment_method=payment_method,
            proof_of_payment=image,
            status=Order.PAID)


class CancelOrder(UpdateAPIView):
    """
    Vista para cancelar una orden de compra.

    Método: PATCH
    Parámetros:
        order_id: id de la orden
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        assert self.request.user == serializer.instance.user
        serializer.save(status=Order.CANCELLED)


class OrdersList(ListAPIView):
    """
    Vista para listar todas las ordenes de compra del usuario.

    Método: GET
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class GetOrder(RetrieveAPIView):
    """
    Vista para obtener una orden de compra del usuario.

    Método: GET
    Parámetros:
        order_id: id de la orden
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]    
    serializer_class = MyOrderSerializer
    model = Order

    def get_object(self):
        order = self.model.objects.get(id=self.kwargs.get('pk'))
        assert self.request.user == order.user
        return order
