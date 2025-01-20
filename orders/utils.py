from datetime import timedelta


from django.db import transaction
from django.db.models import F
from django.utils import timezone

from product.models import Product  
from orders.models import Order, OrderItem


def cancel_old_in_progress_orders():
    """Cancelar ordenes en progreso/ que pasaron de 3 dias."""

    time = timezone.now() - timedelta(days=3)
    orders = Order.objects.filter(status='IN_PROGRESS',
                                  updated_at__lt=time)

    if orders.count() == 0:
        return
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)

        with transaction.atomic():
            for item in order_items:
                product = Product.objects.get(id=item.product.id)
                assert product.stock_on_hold >= item.quantity
                product.stock_on_hold = F('stock_on_hold') - item.quantity
                product.stock = F('stock') + item.quantity
                product.save()

        order.status = 'CANCELLED'
        order.save()

    return
