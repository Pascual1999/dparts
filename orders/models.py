from django.db import IntegrityError, models, transaction
from django.contrib.auth import get_user_model

from product.models import Product
from payment_config.models import PaymentMethod

User = get_user_model()

F = models.F


def upload_to(instance, filename):
    # Capturas seran guardadas en la carpeta perteneciente a 
    # la orden dentro de la carpeta pagos.
    return 'pagos/orden_{instance.id}/{filename}'.format(
        instance=instance, filename=filename)


class Order(models.Model):
    """
    Modelo de Orden
    """
    IN_PROGRESS = 'PRO'
    PAID = 'PAG'
    CANCELLED = 'CAN'
    COMPLETED = 'COM'

    STATUS_CHOICES = {
        IN_PROGRESS: 'En proceso',  # Orden creada, en espera de pago.
        PAID: 'Pagada',      # Orden pagada, en espera de confirmacion.
        CANCELLED: 'Cancelada',   # Orden cancelada.
        COMPLETED: 'Completada'   # Orden completada. Pago confirmado.
    }

    user = models.ForeignKey(
        User, 
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )
    id = models.AutoField(
        primary_key=True
        )
    shipping_address = models.TextField(
        verbose_name="Dirección de Envio",
        null=False,
        blank=False
        )
    contact_number = models.CharField(
        verbose_name="Número de contacto",
        max_length=16,
        null=False,
        blank=False
        )
    status = models.CharField(
        verbose_name="Estado",
        max_length=3,
        choices=STATUS_CHOICES
        )
    amount = models.DecimalField(
        verbose_name="Monto (USD)",
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False
        )
    amount_VEF = models.DecimalField(   
        verbose_name="Monto (VEF)",
        max_digits=12,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )
    IVA = models.DecimalField(
        verbose_name="IVA",
        max_digits=4,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )
    exchange_rate = models.DecimalField(
        verbose_name="Tasa de cambio",
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        verbose_name="Cuenta y metodo al que se pago",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    proof_of_payment = models.ImageField(
        verbose_name="Captura",
        upload_to=upload_to,
        blank=False,
        null=True
        )
    payment_note = models.TextField(
        verbose_name="Nota de pago",
        null=True,
        blank=True
        )
    created_at = models.DateTimeField(
        verbose_name="Creada el",
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        verbose_name="Actualizada el",
        auto_now=True
        )

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('-created_at', '-updated_at')
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'

    def save(self, *args, **kwargs):
        if ((self.status == self.PAID or self.status == self.COMPLETED)
            and (self.proof_of_payment == None)):
            raise Exception('La orden debe tener una captura de pago.')
        else:
            if self.status == self.COMPLETED:
                order_items = OrderItem.objects.filter(order__id=self.id)
                try:
                    with transaction.atomic():
                        for item in order_items:
                            product = Product.objects.get(id=item.product.id)
                            product.stock_on_hold = F('stock_on_hold') - item.quantity
                            product.units_sold = F('units_sold') + item.quantity
                            product.save()
                except IntegrityError:
                    raise Exception('Error al actualizar el stock en reserva.')
            super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Modelo de Item de Orden
    """
    id = models.AutoField(
        primary_key=True
        )
    order = models.ForeignKey(
        Order,
        verbose_name="Orden",
        on_delete=models.CASCADE,
        related_name='items'
        )
    product = models.ForeignKey(
        Product,
        verbose_name="Producto",
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
        )
    product_name = models.CharField(
        verbose_name="Nombre del producto",
        max_length=100,
        null=True,
    )
    quantity = models.IntegerField(
        verbose_name="Cantidad",
        null=False,
        blank=False)
    price = models.DecimalField(
        verbose_name="Precio",
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False
        )

    class Meta:
        verbose_name = "articulo"
        verbose_name_plural = "articulos"

    def __str__(self):
        return 'item_' + '%s' % self.id
    
    def save(self, *args, **kwargs):
        if self.product_name == None:
            self.product_name = self.product.name

        super().save(*args, **kwargs)
