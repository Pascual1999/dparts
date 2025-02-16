from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'product_name', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status',
                    'amount', 'amount_VEF',
                    'exchange_rate', 'created_at',
                    'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ("Información del cliente", {
            "fields": (
                'user',
                'payment_method',
                'shipping_address',
                'contact_number',

                'created_at',
                'updated_at',
            )}
        ),
        ("Información de pago", {
            "fields": (
                'status',
                'IVA',
                'amount',
                'amount_VEF',
                'exchange_rate',
                'proof_of_payment',
            )}
        ),
        )
    readonly_fields = ('user', 'IVA', 'amount', 'amount_VEF', 'exchange_rate', 'created_at', 'updated_at')
    search_fields = ['id', 'status']
    list_filter = ['status', 'created_at', 'updated_at']
    list_per_page = 20



