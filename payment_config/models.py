from django.db import models


class PaymentConfig(models.Model):
    """Modelo para configuraciones de pago.
    Ejemplo: IVA"""
    key = models.CharField(
        max_length=255,
        verbose_name='Clave',
        unique=True,
        null=False,
        blank=False)
    value = models.CharField(
        max_length=255,
        verbose_name='Valor',
        null=False,
        blank=False
        )

    class Meta:
        verbose_name = 'Configuración de pago'
        verbose_name_plural = 'Configuraciones de pago'

    def __str__(self):
        return self.key


class PaymentMethod(models.Model):
    """Modelo para métodos de pago."""
    name = models.CharField(
            max_length=255,
            verbose_name='Nombre del método',
            null=False,
            blank=False
            )
    payment_data = models.TextField(
        verbose_name='Datos',
        blank=False,
        null=False
        )
    is_active = models.BooleanField(
        verbose_name='Activo',
        default=True,
        null=False
        )

    class Meta:
        verbose_name = 'Metodo de pago'
        verbose_name_plural = 'Metodos de pago'

    def __str__(self):
        return self.name


class DollarExchangeHistory(models.Model):
    """Modelo del historial de tasa del dolar."""
    date = models.DateTimeField(
        verbose_name='Fecha',
        null=False,
        blank=False
        )
    value = models.DecimalField(
        verbose_name='Valor',
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False
        )
    page = models.CharField(
        verbose_name='Pagina',
        max_length=64,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Tasa del dolar/historial'
        verbose_name_plural = 'Tasa del dolar/historial'

    def __str__(self):
        return str(self.date.strftime('%Y-%m-%d %H:%M:%S')) + ' - ' + str(self.value) + " Bs."
